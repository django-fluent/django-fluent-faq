from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.views.generic import DetailView, ListView
from fluent_faq.models import FaqCategory, FaqQuestion
from parler.views import TranslatableSlugMixin

if 'fluent_pages' in settings.INSTALLED_APPS:
    # Optional integration with fluent-pages features
    from fluent_pages.views import CurrentPageMixin
else:
    # Simulate basic features for multilingual improvements!
    from parler.views import ViewUrlMixin
    class CurrentPageMixin(ViewUrlMixin):
        pass


class FaqQuestionList(CurrentPageMixin, ListView):
    """
    List view for FAQ questions.
    """
    model = FaqQuestion
    view_url_name = 'faqquestion_index'

    def get_queryset(self):
        return super(FaqQuestionList, self).get_queryset().select_related('category')

    def get_context_data(self, **kwargs):
        context = super(FaqQuestionList, self).get_context_data(**kwargs)
        qs = context['object_list']

        groups = {}
        for obj in qs:
            groups.setdefault(obj.category, []).append(obj)

        categories = []
        for category in sorted(groups.iterkeys(), key=lambda c: (c.order, c.title)):
            categories.append(
                (category, groups[category])
            )

        context['categories'] = categories
        return context


class FaqCategoryDetail(CurrentPageMixin, TranslatableSlugMixin, DetailView):
    """
    Detail view for FAQ categories.
    """
    model = FaqCategory
    view_url_name = 'faqcategory_detail'


class FaqQuestionDetail(CurrentPageMixin, TranslatableSlugMixin, DetailView):
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
