#!/usr/bin/env python3
"""Safely publish only the NAMNum Louis Vuitton article on an already customized VPS.

Never checks out or rebases the production worktree. Local changes and
untracked files unrelated to this article are intentionally left untouched.

Usage: sudo python3 deploy_lv55_safe.py
"""
from __future__ import annotations

import ast
import datetime as dt
import os
import shutil
import subprocess
import sys
from pathlib import Path

APP = Path("/var/www/numerologist")
REF = "origin/main"
SLUG = "louis-vuitton-lv-55"
TEMPLATE = "tall_project/templates/articles/detail_louis_vuitton.html"
THUMB = "tall_project/static/journey/images/article-lv-55.svg"
MIGRATION = "articles/migrations/0017_add_louis_vuitton_lv55_article.py"

INJECTIONS = {
    "articles/views.py": (
        "CUSTOM_ARTICLE_TEMPLATES = {",
        '    "louis-vuitton-lv-55": "articles/detail_louis_vuitton.html",',
    ),
    "articles/thumbnails.py": (
        "ARTICLE_THUMBNAILS: dict[str, dict[str, str]] = {",
        '''    "louis-vuitton-lv-55": {
        "image": "article-lv-55.svg",
        "big": "55",
        "small": "LV · Louis Vuitton",
        "bg": "#21150e",
        "fg": "#e5c48d",
    },''',
    ),
}


def run(*args: str, cwd: Path | None = None) -> str:
    print("+", " ".join(args[:6]), flush=True)
    return subprocess.check_output(args, cwd=cwd, text=True)


def git_show(path: str) -> str:
    return run("git", "-C", str(APP), "-c", f"safe.directory={APP}", "show", f"{REF}:{path}")


def main() -> None:
    if os.geteuid() != 0:
        sys.exit("Kjør med sudo.")
    if not (APP / "manage.py").exists():
        sys.exit(f"Fant ikke Django-prosjektet på {APP}")
    if not (APP / ".venv/bin/python").exists():
        sys.exit("Fant ikke Python-miljøet; ingen endringer utført.")

    run("sudo", "-u", "www-data", "git", "-c",
        f"safe.directory={APP}", "fetch", "origin", "main", cwd=APP)

    # Validate and download all sources before making any local change.
    upstream_files = {p: git_show(p) for p in (TEMPLATE, THUMB, MIGRATION)}
    planned = {}
    for path, (anchor, value) in INJECTIONS.items():
        original = (APP / path).read_text(encoding="utf-8")
        if value in original:
            planned[path] = original
        elif anchor not in original:
            sys.exit(f"Stopp: fant ikke forventet innsettingspunkt i {path}; ingen endringer utført.")
        else:
            planned[path] = original.replace(anchor, anchor + "\n" + value, 1)

    for path in (TEMPLATE, THUMB):
        target = APP / path
        if target.exists() and target.read_text(encoding="utf-8") != upstream_files[path]:
            sys.exit(f"Stopp: {path} finnes allerede med annet innhold. Ingen endringer utført.")

    root = ast.parse(upstream_files[MIGRATION])
    content = next(
        ast.literal_eval(node.value)
        for node in root.body
        if isinstance(node, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "CONTENT" for t in node.targets)
    )

    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = Path(f"/var/backups/namnum-lv55-{stamp}-{os.getpid()}")
    backup.mkdir(parents=True, exist_ok=False)
    backup.chmod(0o755)
    for path in INJECTIONS:
        destination = backup / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(APP / path, destination)

    for path, data in planned.items():
        target = APP / path
        if target.read_text(encoding="utf-8") != data:
            target.write_text(data, encoding="utf-8")

    for path in (TEMPLATE, THUMB):
        target = APP / path
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(upstream_files[path], encoding="utf-8")
            target.chmod(0o644)

    # Check before any database write; backup protects the tracked files.
    run("sudo", "-u", "www-data", str(APP / ".venv/bin/python"),
        "manage.py", "check", cwd=APP)

    # No migrations are added to the customized production worktree:
    # create/update just the LV article record using the reviewed source text.
    payload = backup / "article_content.txt"
    payload.write_text(content, encoding="utf-8")
    payload.chmod(0o644)
    python_code = (
        "from pathlib import Path\n"
        "from articles.models import Article\n"
        f'content = Path({str(payload)!r}).read_text(encoding="utf-8")\n'
        f'obj, created = Article.objects.update_or_create(slug={SLUG!r}, defaults={{'
        "'title': 'Louis Vuitton: De skjulte tallene bak LV = 55', "
        "'content': content, "
        "'author': 'NAMNum Research · SETAEI'})\n"
        'print("ARTIKKEL:", obj.pk, "opprettet" if created else "oppdatert")\n'
    )
    run("sudo", "-u", "www-data", str(APP / ".venv/bin/python"),
        "manage.py", "shell", "-c", python_code, cwd=APP)
    run("sudo", "-u", "www-data", str(APP / ".venv/bin/python"),
        "manage.py", "collectstatic", "--noinput", cwd=APP)
    run("systemctl", "restart", "numerologist")
    run("systemctl", "is-active", "--quiet", "numerologist")
    print(f"\n✅ LV-siden er satt inn og Django er restartet.")
    print(f"🔒 Originalfiler sikkerhetskopiert i {backup}")
    print("🔗 https://namnum.no/articles/louis-vuitton-lv-55/")
    print("⚠️  Øvrige lokale Git-endringer er bevart og fortsatt ikke commit'et.")


if __name__ == "__main__":
    main()
