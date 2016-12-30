from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.six import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from parler.fields import TranslatedField
from parler.models import TranslatableModel, TranslatedFields
from parler.utils.context import switch_language
from fluent_contents.models import PlaceholderField, ContentItemRelation
from fluent_faq.urlresolvers import faq_reverse
from fluent_faq.managers import FaqQuestionManager, FaqCategoryManager
from fluent_utils.softdeps.taggit import TagsMixin


def _get_current_site():
    return Site.objects.get_current().pk


class FaqBaseModel(TranslatableModel):
    """
    Shared functionality for published content.
    """
    # SEO
    meta_keywords = models.CharField(_('keywords'), max_length=255, blank=True, default='', help_text=_("When this field is not filled in, the the tags will be used."))
    meta_description = models.CharField(_('description'), max_length=255, blank=True, default='', help_text=_("When this field is not filled in, the contents or intro text will be used."))

    # Metadata
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('author'), editable=False)
    creation_date = models.DateTimeField(_('creation date'), editable=False, auto_now_add=True)
    modification_date = models.DateTimeField(_('last modification'), editable=False, auto_now=True)

    parent_site = models.ForeignKey(Site, editable=False, default=_get_current_site)

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return self.default_url

    @property
    def default_url(self):
        """
        The internal implementation of :func:`get_absolute_url`.
        This function can be used when overriding :func:`get_absolute_url` in the settings.
        For example::

            ABSOLUTE_URL_OVERRIDES = {
                'fluent_faq.FaqQuestion': lambda o: "http://example.com" + o.default_url
            }
        """
        with switch_language(self):
            root = faq_reverse('faqquestion_index', ignore_multiple=True, language_code=self.get_current_language())
            return root + self.get_relative_url()

    @property
    def url(self):
        """
        The URL of the entry, provided for template code.
        """
        return self.get_absolute_url()

    def get_relative_url(self):
        raise NotImplementedError("get_relative_url")


@python_2_unicode_compatible
class FaqCategory(FaqBaseModel):
    """
    Topic of the FAQ
    """
    # Be compatible with django-orderable table layout,
    # unfortunately, there isn't a good canonical version of it yet.
    order = models.PositiveIntegerField(db_index=True, blank=True, null=True)

    title = TranslatedField(any_language=True)
    translations = TranslatedFields(
        title = models.CharField(_("title"), max_length=200),
        slug = models.SlugField(_("slug")),
    )

    objects = FaqCategoryManager()

    class Meta:
        verbose_name = _("FAQ Category")
        verbose_name_plural = _("FAQ Categories")
        ordering = ('order', 'creation_date')

    def __str__(self):
        # self.title is configured with any_language=True, so always returns a value.
        return self.title

    def get_relative_url(self):
        return u'{0}/'.format(self.slug)

    @property
    def faq_questions(self):
        """
        Fetch the active FAQ questions in this category.
        """
        return self.questions.active_translations()


@python_2_unicode_compatible
class FaqQuestion(TagsMixin, FaqBaseModel):
    """
    Category in the FAQ.
    """
    # This is a separate model instead of using django-categories because:
    # - content needs to be placed on the category.
    # - the title and slug can be translated!

    # Be compatible with django-orderable table layout,
    # unfortunately, there isn't a good canonical version of it yet.
    order = models.PositiveIntegerField(db_index=True, blank=True, null=True)

    title = TranslatedField(any_language=True)
    translations = TranslatedFields(
        title = models.CharField(_("title"), max_length=200),
        slug = models.SlugField(_("slug")),
    )
    contents = PlaceholderField("faq_answer", verbose_name=_("answer"))
    contentitem_set = ContentItemRelation()  # this makes sure the admin can find all deleted objects too.

    # Organisation
    category = models.ForeignKey(FaqCategory, verbose_name=_("Category"), related_name='questions')

    objects = FaqQuestionManager()

    class Meta:
        verbose_name = _("FAQ Question")
        verbose_name_plural = _("FAQ Questions")
        ordering = ('order', 'creation_date')

    def __str__(self):
        # self.title is configured with any_language=True, so always returns a value.
        return self.title

    def get_relative_url(self):
        """
        Return the link path from the archive page.
        """
        # Return the link style, using the permalink style setting.
        return u'{0}{1}/'.format(self.category.get_relative_url(), self.slug)

    def similar_objects(self, num=None, **filters):
        """
        Find similar objects using related tags.
        """
        #TODO: filter appsettings.FLUENT_FAQ_FILTER_SITE_ID:
        #    filters.setdefault('parent_site', self.parent_site_id)

        # FIXME: Using super() doesn't work, calling directly.
        return TagsMixin.similar_objects(self, num=num, **filters)


def _register_anyurlfield_type():
    try:
        from any_urlfield.models import AnyUrlField
        from any_urlfield.forms.widgets import SimpleRawIdWidget
    except ImportError:
        pass
    else:
        AnyUrlField.register_model(FaqQuestion, widget=SimpleRawIdWidget(FaqQuestion))

if 'any_urlfield' in settings.INSTALLED_APPS:
    _register_anyurlfield_type()
