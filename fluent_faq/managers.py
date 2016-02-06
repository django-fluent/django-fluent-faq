"""
The manager class for the FAQ models
"""
from django.conf import settings
from fluent_faq import appsettings
from parler.managers import TranslatableManager, TranslatableQuerySet

__all__ = (
    'FaqQuestionManager',
    'FaqQuestionQuerySet',
)


class FaqBaseModelQuerySet(TranslatableQuerySet):
    """
    The QuerySet for FAQ models.
    """

    def parent_site(self, site):
        """
        Filter to the given site.
        """
        return self.filter(parent_site=site)

    def published(self):
        """
        Return only published entries for the current site.
        """
        if appsettings.FLUENT_FAQ_FILTER_SITE_ID:
            qs = self.parent_site(settings.SITE_ID)
        else:
            qs = self

        return qs

    def active_translations(self, language_code=None, **translated_fields):
        # overwritten to honor our settings instead of the django-parler defaults
        language_codes = appsettings.FLUENT_FAQ_LANGUAGES.get_active_choices(language_code)
        return self.translated(*language_codes, **translated_fields)


class FaqBaseModelManager(TranslatableManager):
    """
    Shared base logic for all FAQ models.
    """
    queryset_class = FaqBaseModelQuerySet

    def parent_site(self, site):
        """
        Filter to the given site.
        """
        return self.all().parent_site(site)

    def published(self):
        """
        Return only published entries for the current site.
        """
        return self.all().published()


# Reserve the class names for extension later
class FaqCategoryQuerySet(FaqBaseModelQuerySet):
    pass


class FaqCategoryManager(FaqBaseModelManager):
    """
    Extra methods attached to ``FaqCategory.objects`` .
    """
    queryset_class = FaqCategoryQuerySet


class FaqQuestionQuerySet(FaqBaseModelQuerySet):
    pass


class FaqQuestionManager(FaqBaseModelManager):
    """
    Extra methods attached to ``FaqQuestion.objects`` .
    """
    queryset_class = FaqQuestionQuerySet
