from django.conf import settings
from django.template import Library
from tag_parser import template_tag
from tag_parser.basetags import BaseAssignmentOrOutputNode

register = Library()

FaqPage = None
HAS_APP_URLS = 'fluent_pages' in settings.INSTALLED_APPS
if HAS_APP_URLS:
    # HACK: accessing FaqPage directly. Apps are not completely separated this way.
    # Should have some kind of registry and filter system (like middleware) instead.
    from fluent_faq.pagetypes.faqpage.models import FaqPage


@template_tag(register, 'get_faq_url')
class GetFaqUrl(BaseAssignmentOrOutputNode):
    """
    Get the URL of a FAQ question.

    When using django-fluent-pages, this takes the current ``page`` variable into account.
    It makes sure the FAQ question is relative to the current page.

    When django-fluent-pages is not used, using this is identical to calling ``faqquestion.get_absolute_url()``.
    """
    min_args = 1
    max_args = 1
    takes_context = True

    def get_value(self, context, *tag_args, **tag_kwargs):
        entry = tag_args[0]

        if HAS_APP_URLS:
            # If the application supports mounting a BlogPage in the page tree,
            # that can be used as relative start point of the entry.
            page = context.get('page')
            request = context.get('request')
            if page is None and request is not None:
                # HACK: access private django-fluent-pages var
                page = getattr(request, '_current_fluent_page', None)

            if page is not None and isinstance(page, FaqPage):
                return page.get_object_url(entry)

        return entry.get_absolute_url()
