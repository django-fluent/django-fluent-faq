from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _, pgettext
from django.utils import six
from fluent_faq.urlresolvers import faq_reverse
from parler.models import TranslatableModel, TranslatedFields
from fluent_contents.models import PlaceholderField, ContentItemRelation
from fluent_faq import appsettings
from fluent_faq.managers import FaqQuestionManager, FaqCategoryManager


# Optional tagging support
from parler.utils.context import switch_language

TaggableManager = None
if 'taggit_autocomplete_modified' in settings.INSTALLED_APPS:
    from taggit_autocomplete_modified.managers import TaggableManagerAutocomplete as TaggableManager
elif 'taggit' in settings.INSTALLED_APPS:
    from taggit.managers import TaggableManager


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

    parent_site = models.ForeignKey(Site, editable=False, default=Site.objects.get_current)

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


class FaqCategory(FaqBaseModel):
    """
    Topic of the FAQ
    """
    # Be compatible with django-orderable table layout,
    # unfortunately, there isn't a good canonical version of it yet.
    order = models.PositiveIntegerField(db_index=True, blank=True, null=True)

    translations = TranslatedFields(
        title = models.CharField(_("title"), max_length=200),
        slug = models.SlugField(_("slug")),
    )

    objects = FaqCategoryManager()

    class Meta:
        verbose_name = _("FAQ Category")
        verbose_name_plural = _("FAQ Categories")
        ordering = ('order', 'creation_date')

    def __unicode__(self):
        return self.title

    def get_relative_url(self):
        return u'{0}/'.format(self.slug)



class FaqQuestion(FaqBaseModel):
    """
    Category in the FAQ.
    """
    # This is a separate model instead of using django-categories because:
    # - content needs to be placed on the category.
    # - the title and slug can be translated!

    # Be compatible with django-orderable table layout,
    # unfortunately, there isn't a good canonical version of it yet.
    order = models.PositiveIntegerField(db_index=True, blank=True, null=True)

    translations = TranslatedFields(
        title = models.CharField(_("title"), max_length=200),
        slug = models.SlugField(_("slug")),
    )
    contents = PlaceholderField("faq_answer", verbose_name=_("answer"))
    contentitem_set = ContentItemRelation()  # this makes sure the admin can find all deleted objects too.

    # Organisation
    category = models.ForeignKey(FaqCategory, verbose_name=_("Category"), related_name='questions')

    # Make association with tags optional.
    if TaggableManager is not None:
        tags = TaggableManager(blank=True, help_text=_("Tags are used to find related questions"))
    else:
        tags = None

    objects = FaqQuestionManager()

    class Meta:
        verbose_name = _("FAQ Question")
        verbose_name_plural = _("FAQ Questions")
        ordering = ('order', 'creation_date')

    def __unicode__(self):
        return self.title


    def get_relative_url(self):
        """
        Return the link path from the archive page.
        """
        # Return the link style, using the permalink style setting.
        return u'{0}{1}/'.format(self.category.get_relative_url(), self.slug)


    def similar_objects(self, num=None, **filters):
        tags = self.tags
        if not tags:
            return []

        content_type = ContentType.objects.get_for_model(self.__class__)
        filters['content_type'] = content_type

        # can't filter, see
        # - https://github.com/alex/django-taggit/issues/32
        # - http://django-taggit.readthedocs.org/en/latest/api.html#TaggableManager.similar_objects
        #
        # Otherwise this would be possible:
        # return tags.similar_objects(**filters)

        lookup_kwargs = tags._lookup_kwargs()
        lookup_keys = sorted(lookup_kwargs)
        qs = tags.through.objects.values(*lookup_kwargs.keys())
        qs = qs.annotate(n=models.Count('pk'))
        qs = qs.exclude(**lookup_kwargs)
        subq = tags.all()
        qs = qs.filter(tag__in=list(subq))
        qs = qs.order_by('-n')

        # from https://github.com/alex/django-taggit/issues/32#issuecomment-1002491
        if filters is not None:
            qs = qs.filter(**filters)

        if num is not None:
            qs = qs[:num]

        # Normal taggit code continues

        # TODO: This all feels like a bit of a hack.
        items = {}
        if len(lookup_keys) == 1:
            # Can we do this without a second query by using a select_related()
            # somehow?
            f = tags.through._meta.get_field_by_name(lookup_keys[0])[0]
            objs = f.rel.to._default_manager.filter(**{
                "%s__in" % f.rel.field_name: [r["content_object"] for r in qs]
            })
            for obj in objs:
                items[(getattr(obj, f.rel.field_name),)] = obj
        else:
            preload = {}
            for result in qs:
                preload.setdefault(result['content_type'], set())
                preload[result["content_type"]].add(result["object_id"])

            for ct, obj_ids in preload.items():
                ct = ContentType.objects.get_for_id(ct)
                for obj in ct.model_class()._default_manager.filter(pk__in=obj_ids):
                    items[(ct.pk, obj.pk)] = obj

        results = []
        for result in qs:
            obj = items[
                tuple(result[k] for k in lookup_keys)
            ]
            obj.similar_tags = result["n"]
            results.append(obj)
        return results


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
