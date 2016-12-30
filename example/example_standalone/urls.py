import fluent_faq.urls
#import form_designer.urls
import tinymce.urls
import taggit_selectize.urls

from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^admin/apps/tinymce/', include(tinymce.urls)),
    url(r'^admin/apps/tags/', include(taggit_selectize.urls)),
    url(r'^admin/', include(admin.site.urls)),

    #url(r'^forms/', include(form_designer.urls)),

    url(r'', include(fluent_faq.urls)),
]
