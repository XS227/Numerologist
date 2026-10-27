from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from members.report_engine import current_age, root_digit, personal_year
from .copy import COPY
from .engine import profile, compare
from .forms import PersonForm, ProfileForm
from .models import DatingProfile

CONSENT_VERSION = "dating-v1-20261027"


def language(request):
    value = request.GET.get("lang") or request.COOKIES.get("nl_lang") or getattr(request, "LANGUAGE_CODE", "no")
    return "no" if value in {"nb", "nn", "no"} else value if value in COPY else "no"


def decorate_form(form, t):
    for key, field in form.fields.items():
        field.label = t.get({"full_name": "name", "birth_date": "birth"}.get(key, key), key)
        field.widget.attrs["class"] = "field-input"
        if key == "full_name":
            field.widget.attrs.update({"autocomplete": "off", "autocapitalize": "words"})
        if hasattr(field, "choices") and key in {"gender", "seeking", "intent"}:
            field.choices = [(value, t.get(value, label)) for value, label in field.choices]
    # Convert custom validation messages without leaking engine details.
    if form.is_bound:
        form.is_valid()
        for field, errors in form.errors.items():
            for index, message in enumerate(errors):
                if message in t:
                    errors[index] = t[message]
    return form


def calc(record, when):
    return profile(record.full_name, record.birth_date, when)


def decorated_report(left, right, t, when):
    report = compare(left, right, when)
    for component in report["components"]:
        component["label"] = t[component["key"]]
        component["theme_a"] = t["themes"][root_digit(component["a"])]
        component["theme_b"] = t["themes"][root_digit(component["b"])]
        score = component["score"]
        component["reading"] = t["missing"] if score is None else t[
            "strong" if score >= 78 else "stretch" if score <= 45 else "balanced"]
    for year in report["years"]:
        a, b = year["a"], year["b"]
        year["theme_a"], year["theme_b"] = t["themes"][a], t["themes"][b]
        key = "year_different"
        if a == b:
            key = "year_same"
        elif a in {1, 5, 8} and b in {1, 5, 8}:
            key = "year_action"
        elif a in {2, 6, 9} and b in {2, 6, 9}:
            key = "year_care"
        elif a in {4, 7} and b in {4, 7}:
            key = "year_quiet"
        year["reading"] = t[key]
    report["relationship_theme"] = t["themes"][report["relationship_number"]]
    return report


def response(request, **context):
    lang = language(request)
    context.update({"t": COPY[lang], "lang": lang, "today": timezone.localdate()})
    result = render(request, "dating/experiment.html", context)
    result["Cache-Control"] = "private, no-store"
    result["X-Robots-Tag"] = "noindex, nofollow, noarchive"
    result["Referrer-Policy"] = "same-origin"
    return result


@never_cache
def experiment(request):
    t, when = COPY[language(request)], timezone.localdate()
    mode = "pair" if request.POST.get("mode", request.GET.get("mode")) == "pair" else "self"
    left = PersonForm(request.POST if request.method == "POST" else None, prefix="you")
    right = PersonForm(request.POST if request.method == "POST" and mode == "pair" else None, prefix="other")
    context = {"page": "experiment", "mode": mode}
    if request.method == "POST" and left.is_valid() and (mode != "pair" or right.is_valid()):
        primary = profile(left.cleaned_data["full_name"], left.cleaned_data["birth_date"], when)
        context["primary"] = primary
        context["numbers"] = [{"label": t[key], "value": primary[key]["kept"] or t["missing"],
                              "theme": t["themes"][primary[key]["root"]]}
                             for key in ("life", "soul", "expression", "maturity")]
        if mode == "pair":
            other = profile(right.cleaned_data["full_name"], right.cleaned_data["birth_date"], when)
            context["report"] = decorated_report(primary, other, t, when)
        else:
            context["solo_years"] = [
                {"year": year, "number": personal_year(primary["birth_date"], year)}
                for year in range(when.year, when.year + 3)]
            for item in context["solo_years"]:
                item["theme"] = t["themes"][item["number"]]
    context.update({"left": decorate_form(left, t), "right": decorate_form(right, t)})
    return response(request, **context)


@login_required(login_url="/min-side/login/")
@never_cache
def edit_profile(request):
    t = COPY[language(request)]
    instance = DatingProfile.objects.filter(user=request.user).first()
    form = ProfileForm(request.POST if request.method == "POST" else None, instance=instance)
    if request.method == "POST" and form.is_valid():
        record = form.save(commit=False)
        record.user = request.user
        record.consent_version = CONSENT_VERSION
        record.consented_at = timezone.now()
        record.save()
        return redirect("/dating/matches/?lang=" + language(request))
    return response(request, page="profile", profile_form=decorate_form(form, t), has_profile=bool(instance))


def eligible(me, candidate, when):
    if me.pk == candidate.pk or not me.is_visible or not candidate.is_visible:
        return False
    if not me.consent_version or not candidate.consent_version:
        return False
    a, b = current_age(me.birth_date.isoformat(), when), current_age(candidate.birth_date.isoformat(), when)
    return (18 <= a <= 120 and 18 <= b <= 120
            and me.min_age <= b <= me.max_age and candidate.min_age <= a <= candidate.max_age
            and me.seeking in {"any", candidate.gender} and candidate.seeking in {"any", me.gender}
            and me.intent == candidate.intent)


def pool(me, when):
    # Apply mutual categorical preferences in SQL, age in Python to handle leap birthdays.
    candidates = DatingProfile.objects.filter(is_visible=True, user__is_active=True,
        intent=me.intent).exclude(user=me.user).filter(Q(seeking="any") | Q(seeking=me.gender))
    if me.seeking != "any":
        candidates = candidates.filter(gender=me.seeking)
    return (candidate for candidate in candidates.iterator() if eligible(me, candidate, when))


@login_required(login_url="/min-side/login/")
@never_cache
def matches(request):
    me = DatingProfile.objects.filter(user=request.user).first()
    if me is None:
        return redirect("/dating/profile/?lang=" + language(request))
    when = timezone.localdate()
    primary = calc(me, when)
    results = []
    if me.is_visible:
        for candidate in pool(me, when):
            candidate_numbers = calc(candidate, when)
            report = compare(primary, candidate_numbers, when)
            results.append({"id": candidate.pk, "alias": candidate.alias, "city": candidate.city,
                            "age": current_age(candidate.birth_date.isoformat(), when),
                            "score": report["score"], "life": candidate_numbers["life"]["kept"]})
    results.sort(key=lambda item: (-(item["score"] or 0), item["id"]))
    return response(request, page="matches", results=results[:50], me=me)


@login_required(login_url="/min-side/login/")
@never_cache
def connection(request, pk):
    me = get_object_or_404(DatingProfile, user=request.user)
    candidate = get_object_or_404(DatingProfile, pk=pk, user__is_active=True)
    when = timezone.localdate()
    if not eligible(me, candidate, when):
        raise Http404
    t = COPY[language(request)]
    return response(request, page="connection", candidate_alias=candidate.alias,
                    report=decorated_report(calc(me, when), calc(candidate, when), t, when))


@login_required(login_url="/min-side/login/")
@require_POST
def delete_profile(request):
    DatingProfile.objects.filter(user=request.user).delete()
    return redirect("/dating/?lang=" + language(request))
