from __future__ import annotations

import base64
import hashlib
import json
import secrets
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, timedelta
from typing import Any

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import csrf_exempt

from .catalog import ACADEMY_LEVELS, PACKAGE_CATALOG, PREMIUM_RESOURCES
from .models import AcademyProgress, MemberProfile, SocialIdentity, SocialLoginHandoff
from .order_bridge import order_for_user, orders_for_user
from .report_engine import calculate_profile


def _safe_next(request: HttpRequest, default: str = "/min-side/") -> str:
    candidate = request.GET.get("next") or request.session.get("member_login_next") or default
    if url_has_allowed_host_and_scheme(candidate, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        return candidate
    return default


def _remember_next(request: HttpRequest) -> None:
    candidate = request.GET.get("next", "")
    if candidate and url_has_allowed_host_and_scheme(candidate, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        request.session["member_login_next"] = candidate


def _profile_for(user: User, *, name: str = "", phone: str = "", picture: str = "") -> MemberProfile:
    profile, _ = MemberProfile.objects.get_or_create(user=user)
    changed = False
    if name and profile.display_name != name:
        profile.display_name = name[:160]
        changed = True
    if phone and profile.phone != phone:
        profile.phone = phone[:40]
        changed = True
    if picture and profile.picture_url != picture:
        profile.picture_url = picture[:200]
        changed = True
    if changed:
        profile.save()
    return profile


def _find_or_create_social_user(provider: str, info: dict[str, Any]) -> User:
    subject = str(info.get("sub") or "").strip()
    if not subject:
        raise ValueError("Missing social identity subject")

    identity = SocialIdentity.objects.select_related("user").filter(provider=provider, subject=subject).first()
    if identity:
        user = identity.user
    else:
        email = str(info.get("email") or "").strip().lower()
        phone = str(info.get("phone_number") or info.get("phone") or "").strip()
        user = User.objects.filter(email__iexact=email).first() if email else None
        if user is None and phone:
            existing_profile = MemberProfile.objects.filter(phone=phone).select_related("user").first()
            user = existing_profile.user if existing_profile else None
        if user is None:
            token = hashlib.sha256(f"{provider}:{subject}".encode()).hexdigest()[:30]
            user = User.objects.create_user(username=f"{provider}_{token}", email=email)
            user.set_unusable_password()
        identity = SocialIdentity.objects.create(
            user=user,
            provider=provider,
            subject=subject,
            email=email,
            phone=phone,
        )

    email = str(info.get("email") or "").strip().lower()
    if email and not user.email:
        user.email = email
        user.save(update_fields=["email"])

    full_name = str(info.get("name") or "").strip()
    if not full_name:
        full_name = " ".join(
            x for x in (str(info.get("given_name") or "").strip(), str(info.get("family_name") or "").strip()) if x
        )
    _profile_for(
        user,
        name=full_name,
        phone=str(info.get("phone_number") or info.get("phone") or "").strip(),
        picture=str(info.get("picture") or "").strip(),
    )
    return user


def _oauth_post(url: str, data: dict[str, str], headers: dict[str, str] | None = None) -> dict[str, Any]:
    encoded = urllib.parse.urlencode(data).encode()
    request = urllib.request.Request(url, data=encoded, headers=headers or {}, method="POST")
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode())


def _oauth_get_json(url: str, headers: dict[str, str]) -> dict[str, Any]:
    request = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode())


def member_login(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect(_safe_next(request))
    _remember_next(request)
    return render(
        request,
        "members/login.html",
        {
            "google_enabled": bool(settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET),
            "vipps_enabled": bool(
                settings.VIPPS_LOGIN_ENABLED
                and (
                    settings.VIPPS_LOGIN_BROKER_URL
                    or (
                        settings.VIPPS_LOGIN_CLIENT_ID
                        and settings.VIPPS_LOGIN_CLIENT_SECRET
                        and settings.VIPPS_LOGIN_MSN
                    )
                )
            ),
            "vipps_test_mode": settings.VIPPS_TEST_MODE,
        },
    )


def member_logout(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("/")


def google_start(request: HttpRequest) -> HttpResponse:
    if not (settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET):
        messages.error(request, "Google-innlogging er klar i koden, men Google OAuth-nøkler mangler på serveren.")
        return redirect("members:login")
    _remember_next(request)
    state = secrets.token_urlsafe(32)
    request.session["google_oauth_state"] = state
    redirect_uri = settings.GOOGLE_REDIRECT_URI or request.build_absolute_uri(reverse("members:google_callback"))
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "prompt": "select_account",
    }
    return redirect("https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params))


def google_callback(request: HttpRequest) -> HttpResponse:
    expected = request.session.pop("google_oauth_state", "")
    state = request.GET.get("state", "")
    code = request.GET.get("code", "")
    if not expected or not secrets.compare_digest(expected, state) or not code:
        messages.error(request, "Google-innlogging kunne ikke bekreftes.")
        return redirect("members:login")
    redirect_uri = settings.GOOGLE_REDIRECT_URI or request.build_absolute_uri(reverse("members:google_callback"))
    try:
        token = _oauth_post(
            "https://oauth2.googleapis.com/token",
            {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri,
            },
            {"Content-Type": "application/x-www-form-urlencoded"},
        )
        info = _oauth_get_json(
            "https://openidconnect.googleapis.com/v1/userinfo",
            {"Authorization": f"Bearer {token['access_token']}"},
        )
        user = _find_or_create_social_user("google", info)
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    except (KeyError, ValueError, urllib.error.URLError, urllib.error.HTTPError) as exc:
        messages.error(request, f"Google-innlogging feilet: {exc}")
        return redirect("members:login")
    return redirect(request.session.pop("member_login_next", "/min-side/"))


def vipps_start(request: HttpRequest) -> HttpResponse:
    if not settings.VIPPS_LOGIN_ENABLED:
        messages.error(request, "Vipps Login er ikke aktivert på serveren ennå.")
        return redirect("members:login")

    _remember_next(request)
    broker_url = str(getattr(settings, "VIPPS_LOGIN_BROKER_URL", "") or "").strip()
    if broker_url:
        next_url = request.session.get("member_login_next", "/min-side/")
        params = urllib.parse.urlencode({"next": next_url})
        return redirect(broker_url + ("&" if "?" in broker_url else "?") + params)

    if not (
        settings.VIPPS_LOGIN_CLIENT_ID
        and settings.VIPPS_LOGIN_CLIENT_SECRET
        and settings.VIPPS_LOGIN_MSN
    ):
        messages.error(request, "Vipps Login er ikke konfigurert på serveren.")
        return redirect("members:login")

    state = secrets.token_urlsafe(32)
    nonce = secrets.token_urlsafe(24)
    request.session["vipps_oauth_state"] = state
    request.session["vipps_oauth_nonce"] = nonce
    redirect_uri = request.build_absolute_uri(reverse("members:vipps_callback"))
    params = {
        "client_id": settings.VIPPS_LOGIN_CLIENT_ID,
        "response_type": "code",
        "scope": "openid name phoneNumber email",
        "state": state,
        "nonce": nonce,
        "redirect_uri": redirect_uri,
    }
    endpoint = settings.VIPPS_LOGIN_BASE_URL + "/access-management-1.0/access/oauth2/auth?"
    return redirect(endpoint + urllib.parse.urlencode(params))


def vipps_callback(request: HttpRequest) -> HttpResponse:
    expected = request.session.pop("vipps_oauth_state", "")
    state = request.GET.get("state", "")
    code = request.GET.get("code", "")
    if not expected or not secrets.compare_digest(expected, state) or not code:
        messages.error(request, "Vipps-innlogging kunne ikke bekreftes.")
        return redirect("members:login")
    redirect_uri = request.build_absolute_uri(reverse("members:vipps_callback"))
    basic = base64.b64encode(
        f"{settings.VIPPS_LOGIN_CLIENT_ID}:{settings.VIPPS_LOGIN_CLIENT_SECRET}".encode()
    ).decode()
    headers = {
        "Authorization": f"Basic {basic}",
        "Merchant-Serial-Number": settings.VIPPS_LOGIN_MSN,
        "Vipps-System-Name": "Numerologist",
        "Vipps-System-Version": "1.0",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    try:
        token = _oauth_post(
            settings.VIPPS_LOGIN_BASE_URL + "/access-management-1.0/access/oauth2/token",
            {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
            },
            headers,
        )
        info = _oauth_get_json(
            settings.VIPPS_LOGIN_BASE_URL + "/vipps-userinfo-api/userinfo/",
            {"Authorization": f"Bearer {token['access_token']}"},
        )
        user = _find_or_create_social_user("vipps", info)
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    except (KeyError, ValueError, urllib.error.URLError, urllib.error.HTTPError) as exc:
        messages.error(request, f"Vipps-innlogging feilet: {exc}")
        return redirect("members:login")
    return redirect(request.session.pop("member_login_next", "/min-side/"))


@csrf_exempt
def vipps_broker_handoff(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({"error": "method_not_allowed"}, status=405)
    if request.META.get("REMOTE_ADDR") not in {"127.0.0.1", "::1"}:
        return JsonResponse({"error": "forbidden"}, status=403)
    try:
        body = json.loads(request.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse({"error": "invalid_json"}, status=400)

    profile = body.get("profile")
    if not isinstance(profile, dict) or not str(profile.get("sub") or "").strip():
        return JsonResponse({"error": "invalid_profile"}, status=400)

    next_url = str(body.get("next") or "/min-side/").strip()
    if not next_url.startswith("/") or next_url.startswith("//"):
        next_url = "/min-side/"

    raw_token = secrets.token_urlsafe(40)
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    SocialLoginHandoff.objects.create(
        token_hash=token_hash,
        provider="vipps",
        payload=profile,
        next_url=next_url[:500],
        expires_at=timezone.now() + timedelta(minutes=5),
    )
    completion = request.build_absolute_uri(
        reverse("members:vipps_complete") + "?" + urllib.parse.urlencode({"token": raw_token})
    )
    return JsonResponse({"completion_url": completion})


def vipps_complete(request: HttpRequest) -> HttpResponse:
    raw_token = request.GET.get("token", "")
    if not raw_token:
        messages.error(request, "Vipps-innlogging kunne ikke fullføres.")
        return redirect("members:login")

    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    handoff = SocialLoginHandoff.objects.filter(
        token_hash=token_hash,
        provider="vipps",
        used_at__isnull=True,
        expires_at__gte=timezone.now(),
    ).first()
    if handoff is None:
        messages.error(request, "Vipps-innloggingen er utløpt eller allerede brukt.")
        return redirect("members:login")

    handoff.used_at = timezone.now()
    handoff.save(update_fields=["used_at"])
    try:
        user = _find_or_create_social_user("vipps", dict(handoff.payload or {}))
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    except (KeyError, ValueError) as exc:
        messages.error(request, f"Vipps-innlogging feilet: {exc}")
        return redirect("members:login")

    next_url = handoff.next_url or "/min-side/"
    if not next_url.startswith("/") or next_url.startswith("//"):
        next_url = "/min-side/"
    return redirect(next_url)


def _ensure_academy(user: User) -> list[AcademyProgress]:
    rows: list[AcademyProgress] = []
    for item in ACADEMY_LEVELS:
        defaults = {"status": "active" if item["level"] == 1 else "locked", "percent": 0}
        progress, _ = AcademyProgress.objects.get_or_create(user=user, level=item["level"], defaults=defaults)
        rows.append(progress)
    return rows


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    profile = _profile_for(request.user)
    orders = orders_for_user(request.user)
    progress = {row.level: row for row in _ensure_academy(request.user)}
    academy = []
    for item in ACADEMY_LEVELS:
        row = progress[item["level"]]
        academy.append({**item, "progress": row})
    return render(
        request,
        "members/dashboard.html",
        {
            "profile": profile,
            "orders": orders,
            "academy": academy,
            "package_catalog": PACKAGE_CATALOG,
        },
    )


def academy(request: HttpRequest) -> HttpResponse:
    progress_map: dict[int, AcademyProgress] = {}
    if request.user.is_authenticated:
        progress_map = {row.level: row for row in _ensure_academy(request.user)}
    levels = []
    for item in ACADEMY_LEVELS:
        levels.append({**item, "progress": progress_map.get(item["level"])})
    return render(request, "members/academy.html", {"levels": levels})


def academy_level(request: HttpRequest, level: int) -> HttpResponse:
    item = next((x for x in ACADEMY_LEVELS if x["level"] == level), None)
    if not item:
        raise Http404
    progress = None
    unlocked = level == 1
    if request.user.is_authenticated:
        progress = next((x for x in _ensure_academy(request.user) if x.level == level), None)
        unlocked = bool(progress and progress.status != "locked")
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(f"{reverse('members:login')}?next={request.path}")
        if not unlocked:
            messages.error(request, "Fullfør forrige nivå først.")
            return redirect("members:academy_level", level=level)
        action = request.POST.get("action")
        if action == "save_homework":
            progress.homework = request.POST.get("homework", "")[:12000]
            progress.percent = max(progress.percent, 80 if progress.homework.strip() else 50)
            progress.status = "active"
            progress.save()
            messages.success(request, "Leksen er lagret.")
        elif action == "complete":
            progress.percent = 100
            progress.status = "completed"
            progress.save()
            next_progress = AcademyProgress.objects.filter(user=request.user, level=level + 1).first()
            if next_progress and next_progress.status == "locked":
                next_progress.status = "active"
                next_progress.save(update_fields=["status", "updated_at"])
            messages.success(request, "Nivået er fullført. Neste nivå er åpnet.")
        return redirect("members:academy_level", level=level)
    resources = [
        {"slug": slug, **resource}
        for slug, resource in PREMIUM_RESOURCES.get(level, {}).items()
    ]
    return render(
        request,
        "members/academy_level.html",
        {"level": item, "progress": progress, "unlocked": unlocked, "premium_resources": resources},
    )


@login_required
def premium_resource(request: HttpRequest, level: int, resource_slug: str) -> HttpResponse:
    item = next((x for x in ACADEMY_LEVELS if x["level"] == level), None)
    resource = PREMIUM_RESOURCES.get(level, {}).get(resource_slug)
    if not item or not resource:
        raise Http404
    progress = next((x for x in _ensure_academy(request.user) if x.level == level), None)
    if not progress or progress.status == "locked":
        messages.error(request, "Denne premiumressursen åpnes når nivået blir aktivt.")
        return redirect("members:academy_level", level=level)
    return render(request, "members/premium_resource.html", {"level": item, "resource": resource})


def _demo_data() -> dict[str, str]:
    return {
        "birth_name": "Kari Elise Nordmann",
        "current_name": "Kari Nordmann",
        "birth_date": "1984-01-15",
        "address": "Storgata 8, Oslo",
        "phone": "+47 952 73 772",
    }


def _report_sections(package_slug: str, profile: dict[str, Any]) -> list[dict[str, Any]]:
    core = [
        {
            "title": "Det første jeg legger merke til",
            "lead": f"Livsveien {profile['life']['label']} møter navnetallet {profile['expression']['label']}.",
            "body": "Dette er ikke én etikett, men to lag som må leses sammen: retningen livet presser deg mot, og måten du naturlig uttrykker deg på.",
        },
        {
            "title": "Indre og ytre lag",
            "lead": f"Vokaltall {profile['soul']['label']} · konsonanttall {profile['personality']['label']}",
            "body": "Her ser vi forskjellen mellom hva som trekker deg innenfra og det første uttrykket andre vanligvis møter.",
        },
    ]
    timing = [
        {
            "title": "Timingen nå",
            "lead": f"Personlig år {profile['personal_year']} · måned {profile['personal_month']} · essens {profile['essence']['label']}",
            "body": "Når kortere og lengre sykluser peker samme vei, blir temaet tydeligere. I en full rapport brytes dette videre ned måned for måned.",
        },
        {
            "title": "Den lange buen",
            "lead": " → ".join(x["label"] for x in profile["pinnacles"]),
            "body": f"Utviklingstrinnene leses sammen med livsperiodene {' · '.join(map(str, profile['life_cycles']))} og realiseringstallet {profile['maturity']['label']}.",
        },
    ]
    partner = [
        {
            "title": "To komplette kart",
            "lead": "Navnelag + livsveilag + timing",
            "body": "Partneranalysen skal aldri reduseres til én kompatibilitetsbokstav. Digitalversjonen viser begge personer separat før relasjonen syntetiseres.",
        },
        {
            "title": "Relasjonens språk",
            "lead": "Likheter · forskjeller · timing",
            "body": "Her skal rapporten vise hva som flyter naturlig, hvor ulike behov møtes, og hva som er aktivt i relasjonen nå.",
        },
    ]
    if package_slug == "ase227":
        return core + timing + [
            {
                "title": "Komplett tallkart",
                "lead": f"Utfordringer {' · '.join(map(str, profile['challenges']))}",
                "body": "Alle enkeltberegninger ligger tilgjengelig som dokumentasjon bak den personlige fortellingen.",
            }
        ]
    if package_slug == "personlighet":
        return core + [{"title": "Åses personlige syntese", "lead": "Menneskelig fordypning", "body": "Denne delen viser hvor Åses egen formulering og caseforståelse kommer inn etter den automatiske grunnrapporten."}]
    if package_slug == "fremtid2":
        return timing + [{"title": "24 måneder", "lead": "Måned-for-måned", "body": "Digitalversjonen skal inneholde en navigerbar tidslinje for to hele år, med transitter og essenstall overlagt."}]
    if package_slug == "partner":
        return partner + timing[:1]
    if package_slug in {"komplett1", "komplett2", "komplett3"}:
        years = {"komplett1": 1, "komplett2": 2, "komplett3": 3}[package_slug]
        return core + timing + [{"title": f"{years} års fremtidslag", "lead": f"{years * 12} måneder", "body": "Den komplette analysen kombinerer personligheten, livssyklusene og den detaljerte fremtidstidslinjen."}]
    if package_slug == "veiledning15":
        return [
            {"title": "Før samtalen", "lead": f"Livsvei {profile['life']['label']} · navn {profile['expression']['label']}", "body": "Brukeren får et kort kart og kan skrive tre spørsmål før samtalen."},
            {"title": "Etter samtalen", "lead": "Notater og neste steg", "body": "Den digitale versjonen blir et sted å lagre Åses hovedpoenger og lenker til relevant læring."},
        ]
    if package_slug == "familie3":
        return [
            {"title": "Person 1", "lead": "Komplett rapport + 1 år", "body": "Egen rapport og tidslinje."},
            {"title": "Person 2", "lead": "Komplett rapport + 1 år", "body": "Egen rapport og tidslinje."},
            {"title": "Person 3", "lead": "Komplett rapport + 1 år", "body": "Egen rapport og tidslinje."},
            {"title": "Felles oversikt", "lead": "Tre rapporter på Min side", "body": "Kjøperen kan åpne hver person separat fra samme ordre."},
        ]
    return core


def report_demo(request: HttpRequest, package_slug: str) -> HttpResponse:
    package = PACKAGE_CATALOG.get(package_slug)
    if not package:
        raise Http404
    data = _demo_data()
    profile = calculate_profile(data)
    return render(
        request,
        "members/report.html",
        {
            "package": package,
            "package_slug": package_slug,
            "profile": profile,
            "sections": _report_sections(package_slug, profile),
            "demo": True,
            "order": None,
        },
    )


@login_required
def report_view(request: HttpRequest, order_id: str) -> HttpResponse:
    order = order_for_user(request.user, order_id)
    if not order:
        raise Http404
    if not order["digital_available"]:
        messages.info(request, "Digitalversjonen åpnes så snart betalingen er registrert.")
        return redirect("members:dashboard")
    profile = calculate_profile(order)
    return render(
        request,
        "members/report.html",
        {
            "package": order["product"],
            "package_slug": order["package"],
            "profile": profile,
            "sections": _report_sections(order["package"], profile),
            "demo": False,
            "order": order,
        },
    )
