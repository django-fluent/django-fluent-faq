from os.path import join, dirname
from example_standalone.settings import *

INSTALLED_APPS += (
    # Add fluent pages with a simple page type:
    'fluent_pages',
    #'fluent_pages.pagetypes.fluentpage',
    'fluent_pages.pagetypes.flatpage',

    # Add the page type for adding the "faq" root to the page tree.
    'fluent_faq.pagetypes.faqpage',

    # fluent-pages dependencies:
    'polymorphic',
    'polymorphic_tree',
)

ROOT_URLCONF = 'example_fluent_pages.urls'

if django.VERSION >= (1, 8):
    TEMPLATES[0]['DIRS'] = [
        join(dirname(__file__), "templates"),
    ]
else:
    TEMPLATE_DIRS = (
        join(dirname(__file__), "templates"),
    )
