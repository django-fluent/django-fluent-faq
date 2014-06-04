from django.contrib import admin
from fluent_faq.models import FaqCategory, FaqQuestion
from .faqcategoryadmin import FaqCategoryAdmin
from .faqquestionadmin import FaqQuestionAdmin

admin.site.register(FaqCategory, FaqCategoryAdmin)
admin.site.register(FaqQuestion, FaqQuestionAdmin)
