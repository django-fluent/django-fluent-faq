from django.conf.urls import url
from .views import FaqQuestionList, FaqCategoryDetail, FaqQuestionDetail

urlpatterns = [
    url(r'^$', FaqQuestionList.as_view(), name='faqquestion_index'),
    url(r'^(?P<slug>[^/]+)/$', FaqCategoryDetail.as_view(), name='faqcategory_detail'),
    url(r'^(?P<cat_slug>[^/]+)/(?P<slug>[^/]+)/$', FaqQuestionDetail.as_view(), name='faqquestion_detail'),
]
