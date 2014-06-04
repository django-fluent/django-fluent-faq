from django.http import HttpResponsePermanentRedirect
from django.views.generic import DetailView, ListView
from fluent_faq.models import FaqCategory, FaqQuestion
from parler.views import TranslatableSlugMixin


class FaqQuestionList(ListView):
    """
    List view for FAQ questions.
    """
    model = FaqQuestion

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


class FaqCategoryDetail(TranslatableSlugMixin, DetailView):
    """
    Detail view for FAQ categories.
    """
    model = FaqCategory
    slug_url_kwarg = 'cat_slug'


class FaqQuestionDetail(TranslatableSlugMixin, DetailView):
    """
    Detail view for FAQ questions.
    """
    model = FaqQuestion

    def render_to_response(self, context, **response_kwargs):
        """
        Make sure the view opens at the canonical URL, or redirect otherwise.
        """
        # Redirect to the canonical URL when the category slug is incorrect.
        if self.kwargs['cat_slug'] != self.object.category.slug:
            # NOTE: this doesn't deal with multiple root nodes yet.
            return HttpResponsePermanentRedirect(self.object.get_absolute_url())

        return super(FaqQuestionDetail, self).render_to_response(context, **response_kwargs)
