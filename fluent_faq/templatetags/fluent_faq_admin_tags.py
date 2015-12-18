from django.template import Library
from fluent_faq.admin import FaqQuestionAdmin

register = Library()


@register.simple_tag()
def actions_column(faqquestion):
    return FaqQuestionAdmin.get_actions_column(faqquestion)
