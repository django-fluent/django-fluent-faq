from django.contrib.sitemaps import Sitemap
from fluent_faq.models import FaqCategory, FaqQuestion
from fluent_faq.urlresolvers import faq_reverse


class FaqQuestionSitemap(Sitemap):
    """
    Sitemap for FAQ questions
    """
    def items(self):
        return FaqQuestion.objects.published()

    def lastmod(self, category):
        """Return the last modification of the object."""
        return category.modification_date

    def location(self, category):
        """Return url of an question."""
        return faq_reverse('faqcategory_detail', kwargs={'slug': category.slug}, ignore_multiple=True)



class FaqCategorySitemap(Sitemap):
    """
    Sitemap for FAQ categories.
    """
    def items(self):
        return FaqCategory.objects.published()

    def lastmod(self, category):
        """Return the last modification of the object."""
        return category.modification_date

    def location(self, category):
        """Return url of an category."""
        return faq_reverse('faqcategory_detail', kwargs={'slug': category.slug}, ignore_multiple=True)
