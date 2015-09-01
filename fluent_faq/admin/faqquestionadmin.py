import django
from fluent_faq.admin.base import FaqBaseModelAdmin
from fluent_faq.models import FaqQuestion


class FaqQuestionAdmin(FaqBaseModelAdmin):
    """
    Admin interface for the FAQ Question model.
    """
    list_display = ('title', 'language_column', 'category', 'modification_date', 'actions_column')
    list_filter = ('category',)

    FIELDSET_GENERAL = (None, {
        'fields': ('title', 'slug', 'contents',),
    })

    fieldsets = (
        FIELDSET_GENERAL,
        FaqBaseModelAdmin.FIELDSET_PUBLICATION,
        FaqBaseModelAdmin.FIELDSET_SEO,
    )

    def get_queryset(self, request):
        return super(FaqQuestionAdmin, self).get_queryset(request).select_related('category')

    if django.VERSION < (1,6):
        queryset = get_queryset


# Add all fields
for _f in ('category', 'tags'):
    if _f in FaqQuestion._meta.get_all_field_names():
        FaqQuestionAdmin.FIELDSET_GENERAL[1]['fields'] += (_f,)
