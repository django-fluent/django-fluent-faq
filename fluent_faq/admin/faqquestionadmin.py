import django
from fluent_faq.admin.base import FaqBaseModelAdmin
from fluent_faq.models import FaqQuestion

if django.VERSION >= (1, 8):
    # get_all_field_names() was deprecated
    _model_fields = [f.name for f in FaqQuestion._meta.get_fields()]
else:
    # This also returns any _id fields, but that's not an issue for us here.
    _model_fields = FaqQuestion._meta.get_all_field_names()


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

    if django.VERSION < (1, 6):
        queryset = get_queryset


# Add all fields
for _f in ('category', 'tags'):
    if _f in _model_fields:
        FaqQuestionAdmin.FIELDSET_GENERAL[1]['fields'] += (_f,)
