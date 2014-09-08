from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import NoReverseMatch
from fluent_faq.models import FaqCategory, FaqQuestion
from fluent_faq.urlresolvers import faq_reverse


def _url_patterns_installed():
    # This module can use normal Django urls.py URLs, or mount the "FaqPage" in the page tree.
    # Check whether the URLs are installed, so the `sitemap.xml` can be generated nevertheless.
    # This issue will pop up elsewhere too, so there is no need to raise an error here.
    try:
        faq_reverse('faqcategory_detail', kwargs={'slug': 'category'}, ignore_multiple=True)
    except NoReverseMatch:
        return False
    else:
        return True


class FaqQuestionSitemap(Sitemap):
    """
    Sitemap for FAQ questions
    """
    def items(self):
        if not _url_patterns_installed():
            return None
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
        if not _url_patterns_installed():
            return None
        return FaqCategory.objects.published()

    def lastmod(self, category):
        """Return the last modification of the object."""
        return category.modification_date

    def location(self, category):
        """Return url of an category."""
        return faq_reverse('faqcategory_detail', kwargs={'slug': category.slug}, ignore_multiple=True)
