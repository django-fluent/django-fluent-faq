from fluent_pages.extensions import page_type_pool, PageTypePlugin
from .admin import FaqPageAdmin
from .models import FaqPage


@page_type_pool.register
class FaqPagePlugin(PageTypePlugin):
    """
    Plugin binding the FaqPage model as pagetype.
    """
    model = FaqPage
    model_admin = FaqPageAdmin
    urls = 'fluent_faq.urls'
