from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.views.generic import DetailView, ListView
from fluent_utils.softdeps.fluent_pages import CurrentPageMixin
from fluent_faq.models import FaqCategory, FaqQuestion
from parler.views import TranslatableSlugMixin


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

    def get_template_names(self):
        names = super(FaqQuestionList, self).get_template_names()  # faqquestion_list.html
        names.insert(0, "fluent_faq/index.html")
        return names


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
