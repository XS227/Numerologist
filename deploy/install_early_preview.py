"""Install the gate on the existing hybrid PHP/Django nginx vhost.

Run as root after restarting Django. nginx -t validates before reload; restore
the original configuration on failure. No other vhost is changed.
"""
import os
from pathlib import Path
import re
import subprocess
import sys

MARKER = "# Numerologist early preview v1"
HOSTS = {"numerologist.setai.no", "numerologist.setaei.com"}


def blocks(text):
    """Brace pairs, ignoring quoted values and comments."""
    stack, pairs = [], []
    quote, comment, escaped = None, False, False
    for i, char in enumerate(text):
        if comment:
            if char == "\n":
                comment = False
            continue
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if quote:
            if char == quote:
                quote = None
            continue
        if char in "\"'":
            quote = char
        elif char == "#":
            comment = True
        elif char == "{":
            stack.append(i)
        elif char == "}":
            if not stack:
                raise ValueError("Unbalanced nginx config")
            pairs.append((stack.pop(), i))
    if stack:
        raise ValueError("Unbalanced nginx config")
    return pairs


def install(text):
    if MARKER in text:
        return text
    edits = []
    matches = 0
    for start, end in blocks(text):
        prefix = re.sub(r"(?m)#.*$", "", text[:start])
        if not re.search(r"(?:^|[;{}])\s*server\s*$", prefix):
            continue
        body = text[start + 1:end]
        names = re.search(r"\bserver_name\s+([^;]+);", body)
        if not names or not (set(names[1].split()) & HOSTS):
            continue
        # HTTP redirect-only servers carry no project content.
        upstreams = set(re.findall(r"\bproxy_pass\s+(http://[^;\s]+);", body))
        if not upstreams:
            if re.search(r"\breturn\s+30[1278]\s+https://", body):
                continue
            raise ValueError("Numerologist server has no identifiable Django upstream")
        if len(upstreams) != 1:
            raise ValueError("Multiple proxy upstreams: inspect the vhost before installing")
        if re.search(r"\b(?:auth_request|satisfy)\s", body):
            raise ValueError("Existing access rules need manual integration")
        upstream = upstreams.pop()
        if not (re.fullmatch(r"http://[\w.:-]+/?", upstream)
                or re.fullmatch(r"http://unix:/[^:]+:", upstream)):
            raise ValueError("Unsupported proxy_pass URI; inspect the vhost")
        upstream = upstream.rstrip("/")
        snippet = f'''
    {MARKER}
    auth_request /early-preview/auth/;
    error_page 401 = /early-preview/;
    add_header X-Robots-Tag "noindex, nofollow, noarchive" always;
    add_header Cache-Control "private, no-store, max-age=0" always;
    location = /early-preview/auth/ {{
        internal;
        auth_request off;
        proxy_pass {upstream};
        proxy_method GET;
        proxy_pass_request_body off;
        proxy_set_header Content-Length "";
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Cookie $http_cookie;
        proxy_cache off;
    }}
    location = /early-preview/ {{
        auth_request off;
        proxy_pass {upstream};
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Preview-Return $request_uri;
        proxy_cache off;
    }}
'''
        edits.append((end, snippet))
        matches += 1
    if not matches:
        raise ValueError("No Numerologist content server found")
    for position, snippet in sorted(edits, reverse=True):
        text = text[:position] + snippet + text[position:]
    return text


def main():
    if os.geteuid() != 0:
        raise SystemExit("Run as root")
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "/etc/nginx/sites-available/numerologist").resolve()
    original = path.read_text()
    updated = install(original)
    if updated == original:
        print("Early preview nginx gate already installed")
        return
    backup = path.with_name(path.name + ".before-early-preview")
    if not backup.exists():
        backup.write_text(original)
    path.write_text(updated)
    try:
        subprocess.run(["nginx", "-t"], check=True)
        subprocess.run(["systemctl", "reload", "nginx"], check=True)
    except Exception:
        path.write_text(original)
        subprocess.run(["nginx", "-t"], check=False)
        raise
    print("Early preview enabled for all Numerologist routes")


if __name__ == "__main__":
    main()
