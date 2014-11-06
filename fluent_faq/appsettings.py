from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from parler import appsettings as parler_appsettings
from parler.utils import normalize_language_code, is_supported_django_language

# Advanced settings
FLUENT_FAQ_FILTER_SITE_ID = getattr(settings, 'FLUENT_FAQ_FILTER_SITE_ID', True)
FLUENT_FAQ_BASE_TEMPLATE = getattr(settings, "FLUENT_FAQ_BASE_TEMPLATE", 'fluent_faq/base.html')

# Performance settings
FLUENT_FAQ_PREFETCH_TRANSLATIONS = getattr(settings, 'FLUENT_FAQ_PREFETCH_TRANSLATIONS', False)

# Note: the default language setting is used during the migrations
# Allow this module to have other settings, but default to the shared settings
FLUENT_DEFAULT_LANGUAGE_CODE = getattr(settings, 'FLUENT_DEFAULT_LANGUAGE_CODE', parler_appsettings.PARLER_DEFAULT_LANGUAGE_CODE)
FLUENT_FAQ_DEFAULT_LANGUAGE_CODE = getattr(settings, 'FLUENT_FAQ_DEFAULT_LANGUAGE_CODE', FLUENT_DEFAULT_LANGUAGE_CODE)
FLUENT_FAQ_LANGUAGES = getattr(settings, 'FLUENT_FAQ_LANGUAGES', parler_appsettings.PARLER_LANGUAGES)


# Clean settings
FLUENT_FAQ_DEFAULT_LANGUAGE_CODE = normalize_language_code(FLUENT_FAQ_DEFAULT_LANGUAGE_CODE)

if not is_supported_django_language(FLUENT_FAQ_DEFAULT_LANGUAGE_CODE):
    raise ImproperlyConfigured("FLUENT_FAQ_DEFAULT_LANGUAGE_CODE '{0}' does not exist in LANGUAGES".format(FLUENT_FAQ_DEFAULT_LANGUAGE_CODE))

FLUENT_FAQ_LANGUAGES = parler_appsettings.add_default_language_settings(
    FLUENT_FAQ_LANGUAGES, 'FLUENT_FAQ_LANGUAGES',
    code=FLUENT_FAQ_DEFAULT_LANGUAGE_CODE,
    fallback=FLUENT_FAQ_DEFAULT_LANGUAGE_CODE,
    hide_untranslated=False,
)
