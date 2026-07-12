"""Bridge the PHP site's language choice into Django.

The site is a hybrid: the PHP pages (front page, number pages, content pages)
store the visitor's language in an ``nl_lang`` cookie (values ``no`` / ``en``),
while the Django part (articles, intake, CMS) has its own i18n. Without a
bridge, switching language on the PHP side leaves the Django articles stuck on
the default English — which is exactly the "suddenly English again" the site
owner reported.

This middleware reads ``nl_lang`` and activates the matching Django language
for the request, so the whole site switches together. It runs after
LocaleMiddleware so it has the final say.
"""

from django.utils import translation

_MAP = {"no": "nb", "en": "en"}


class NlLangCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = _MAP.get(request.COOKIES.get("nl_lang", ""))
        if lang:
            translation.activate(lang)
            request.LANGUAGE_CODE = lang
        try:
            return self.get_response(request)
        finally:
            if lang:
                translation.deactivate()
