from django.utils.translation import ugettext_lazy as _
from fluent_faq.models import FaqQuestion
from fluent_pages.models import HtmlPage


class FaqPage(HtmlPage):
    """
    The page root for FAQ questions.
    """

    class Meta:
        verbose_name = _("FAQ module")
        verbose_name_plural = _("FAQ modules")

    @property
    def questions(self):
        """
        Return the entries that are published under this node.
        """
        return FaqQuestion.objects.all()

    def get_object_url(self, object):
        """
        Return the URL of a FaqQuestion, relative to this page.
        """
        return self.get_absolute_url() + object.get_relative_url()
