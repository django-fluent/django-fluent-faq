from django.contrib import admin
from fluent_pages.adminui import HtmlPageAdmin

from .models import FaqPage


@admin.register(FaqPage)
class FaqPageAdmin(HtmlPageAdmin):
    pass

