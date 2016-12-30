import fluent_pages.urls
#import form_designer.urls
import taggit_selectize.urls
import tinymce.urls

from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/apps/tinymce/', include(tinymce.urls)),
    url(r'^admin/apps/tags/', include(taggit_selectize.urls)),
    url(r'^admin/', include(admin.site.urls)),

    #url(r'^forms/', include(form_designer.urls)),

    # Not including fluent_faq.urls.
    # Instead, create a "faqpage" in the page tree.
    # all URLs will be displayed there.
    url(r'', include(fluent_pages.urls)),
]
