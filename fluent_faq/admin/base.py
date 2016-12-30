from django.conf import settings
from django.contrib.admin.widgets import AdminTextInputWidget, AdminTextareaWidget
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.core.urlresolvers import NoReverseMatch
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext, ugettext_lazy as _
from fluent_faq import appsettings
from fluent_contents.admin import PlaceholderFieldAdmin
from fluent_utils.softdeps.fluent_pages import mixed_reverse
from fluent_utils.dry.admin import MultiSiteAdminMixin
from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm
from parler.models import TranslationDoesNotExist


class FaqBaseModelForm(TranslatableModelForm):
    """
    Base form for FAQ questions.
    """

    def clean_slug(self):
        """
        Test whether the slug is unique within the language domain.
        """
        slug = self.cleaned_data['slug']
        dup_qs = self._meta.model.objects.translated(self.language_code, slug=slug)
        if self.instance and self.instance.pk:
            dup_qs = dup_qs.exclude(pk=self.instance.pk)

        if dup_qs.exists():
            raise ValidationError(_("The slug is not unique"))

        return slug


class FaqBaseModelAdmin(MultiSiteAdminMixin, TranslatableAdmin, PlaceholderFieldAdmin):
    """
    Base admin for FAQ questions
    """
    filter_site = appsettings.FLUENT_FAQ_FILTER_SITE_ID
    list_display = ('title', 'language_column', 'modification_date', 'actions_column')
    form = FaqBaseModelForm
    search_fields = ('translations__slug', 'translations__title')

    # Using fieldnames here works because formfield_for_dbfield() is overwritten.
    formfield_overrides = {
        'meta_keywords': {
            'widget': AdminTextInputWidget(attrs={'class': 'vLargeTextField'})
        },
        'meta_description': {
            'widget': AdminTextareaWidget(attrs={'rows': 3})
        },
    }

    FIELDSET_GENERAL = (None, {
        'fields': ('title', 'slug',),
    })
    FIELDSET_PUBLICATION = (_('Publication settings'), {
        'fields': ('order',),
        #'classes': ('collapse',),
    })
    FIELDSET_SEO = (_('SEO settings'), {
        'fields': ('meta_keywords', 'meta_description'),
        'classes': ('collapse',),
    })

    fieldsets = (
        FIELDSET_GENERAL,
        FIELDSET_PUBLICATION,
        FIELDSET_SEO,
    )

    class Media:
        css = {
            'all': ('fluent_faq/admin/admin.css',)
        }

    def get_prepopulated_fields(self, request, obj=None):
        # Needed for django-parler
        return {'slug': ('title',), }

    def save_model(self, request, obj, form, change):
        # Automatically store the user in the author field.
        if not change:
            obj.author = request.user
        obj.save()

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Allow formfield_overrides to contain field names too.
        """
        overrides = self.formfield_overrides.get(db_field.name)
        if overrides:
            kwargs.update(overrides)

        return super(FaqBaseModelAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        # When the page is accessed via a pagetype, warn that the node can't be previewed yet.
        context['preview_error'] = ''
        if 'fluent_pages' in settings.INSTALLED_APPS:
            from fluent_pages.urlresolvers import PageTypeNotMounted, MultipleReverseMatch
            try:
                self._reverse_faqpage_index(request, obj)
            except PageTypeNotMounted:
                from fluent_faq.pagetypes.faqpage.models import FaqPage
                context['preview_error'] = ugettext("The {object_name} can't be previewed yet, a '{page_type_name}' page needs to be created first.").format(object_name=self.model._meta.verbose_name, page_type_name=FaqPage._meta.verbose_name)
            except MultipleReverseMatch:
                # When 'faqquestion_index is ambiguous (because there are multiple FAQ nodes in the fluent-pages tree),
                # the edit page will automatically pick an option.
                pass
            except NoReverseMatch:
                # Since forgetting the pagetype app is easy, give off a warning to help developers
                # find their way with these apps.
                raise ImproperlyConfigured(
                    "To use django-fluent-faq, either include('fluent_faq.urls') in the URLConf, "
                    "or add the 'fluent_faq.pagetypes.faqpage' app to the INSTALLED_APPS."
                )

        return super(FaqBaseModelAdmin, self).render_change_form(request, context, add, change, form_url, obj)

    def _reverse_faqpage_index(self, request, obj=None):
        # Internal method with "protected access" to handle translation differences.
        # This is only called when 'fluent_pages' is in the INSTALLED_APPS.
        return mixed_reverse('faqquestion_index')

    @classmethod
    def get_actions_column(cls, faqquestion):
        return mark_safe(u' '.join(conditional_escape(a) for a in cls._actions_column_icons(faqquestion)))

    @classmethod
    def _actions_column_icons(cls, object):
        actions = []
        if cls.can_preview_object(object):
            try:
                url = object.get_absolute_url()
            except (NoReverseMatch, TranslationDoesNotExist):
                # A FaqQuestion is already added, but the URL can no longer be resolved.
                # This can either mean that urls.py is missing a 'fluent_faq.urls' (unlikely),
                # or that this is a PageTypeNotMounted exception because the "FAQ page" node was removed.
                # In the second case, the edit page should still be reachable, and the "view on site" link will give an alert.
                pass
            else:
                actions.append(mark_safe(
                    u'<a href="{url}" title="{title}" target="_blank"><img src="{static}fluent_faq/img/admin/world.gif" width="16" height="16" alt="{title}" /></a>'.format(
                        url=url, title=_('View on site'), static=settings.STATIC_URL)
                ))
        return actions

    @classmethod
    def can_preview_object(cls, object):
        """ Override whether the node can be previewed. """
        #return hasattr(faqquestion, 'get_absolute_url') and faqquestion.is_published
        return True

    def actions_column(self, faqquestion):
        return self.get_actions_column(faqquestion)

    actions_column.allow_tags = True
    actions_column.short_description = _('Actions')
