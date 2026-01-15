from .models import MultilingualExample
from parler.admin import TranslatableAdmin
from django.contrib import admin


@admin.register(MultilingualExample)
class MultilingualExampleAdmin(TranslatableAdmin):
    list_display = ('title', 'description')