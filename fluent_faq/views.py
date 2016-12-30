from django.http import HttpResponsePermanentRedirect
from django.views.generic import DetailView, ListView
from fluent_faq import appsettings
from fluent_utils.softdeps.fluent_pages import CurrentPageMixin
from fluent_faq.models import FaqCategory, FaqQuestion
from parler.views import TranslatableSlugMixin


class BaseFaqMixin(CurrentPageMixin):
    context_object_name = None
    prefetch_translations = False

    def get_context_data(self, **kwargs):
        context = super(BaseFaqMixin, self).get_context_data(**kwargs)
        context['FLUENT_FAQ_BASE_TEMPLATE'] = appsettings.FLUENT_FAQ_BASE_TEMPLATE
        return context


class FaqQuestionList(BaseFaqMixin, ListView):
    """
    List view for FAQ questions.
    """
    model = FaqQuestion
    view_url_name = 'faqquestion_index'
    prefetch_translations = False

    def get_queryset(self):
        qs = super(FaqQuestionList, self).get_queryset().select_related('category').active_translations()
        if self.prefetch_translations:
            qs = qs.prefetch_related('translations')
        return qs

    def get_context_data(self, **kwargs):
        context = super(FaqQuestionList, self).get_context_data(**kwargs)
        qs = context['object_list']

        groups = {}
        for obj in qs:
            groups.setdefault(obj.category, []).append(obj)

        categories = []
        for category in sorted(groups.keys(), key=lambda c: (c.order, c.title)):
            categories.append(
                (category, groups[category])
            )

        context['categories'] = categories
        return context

    def get_template_names(self):
        names = super(FaqQuestionList, self).get_template_names()  # faqquestion_list.html
        names.insert(0, "fluent_faq/index.html")
        return names


class BaseFaqDetailView(BaseFaqMixin, TranslatableSlugMixin, DetailView):
    # Only relevant at the detail page, e.g. for a language switch menu.
    prefetch_translations = appsettings.FLUENT_FAQ_PREFETCH_TRANSLATIONS

    def get_queryset(self):
        # Not filtering active_languages(), let TranslatableSlugMixin handle everything.
        qs = super(BaseFaqDetailView, self).get_queryset()
        if self.prefetch_translations:
            qs = qs.prefetch_related('translations')
        return qs

    def get_language_choices(self):
        return appsettings.FLUENT_FAQ_LANGUAGES.get_active_choices()


class FaqCategoryDetail(BaseFaqDetailView):
    """
    Detail view for FAQ categories.
    """
    model = FaqCategory
    view_url_name = 'faqcategory_detail'


class FaqQuestionDetail(BaseFaqDetailView):
    """
    Detail view for FAQ questions.
    """
    model = FaqQuestion
    view_url_name = 'faqquestion_detail'

    def render_to_response(self, context, **response_kwargs):
        """
        Make sure the view opens at the canonical URL, or redirect otherwise.
        """
        # Redirect to the canonical URL when the category slug is incorrect.
        if self.kwargs['cat_slug'] != self.object.category.slug:
            # NOTE: this doesn't deal with multiple root nodes yet.
            return HttpResponsePermanentRedirect(self.object.get_absolute_url())

        return super(FaqQuestionDetail, self).render_to_response(context, **response_kwargs)
