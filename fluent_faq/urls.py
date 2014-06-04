from django.conf.urls import patterns, url
from .views import FaqQuestionList, FaqCategoryDetail, FaqQuestionDetail

urlpatterns = patterns('',
    url(r'^$', FaqQuestionList.as_view(), name='faqquestion_index'),
    url(r'^(?P<slug>[^/]+)/$', FaqCategoryDetail.as_view(), name='faqcategory_detail'),
    url(r'^(?P<cat_slug>[^/]+)/(?P<slug>[^/]+)/$', FaqQuestionDetail.as_view(), name='faqquestion_detail'),
)
