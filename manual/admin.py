from django.contrib import admin
from .models import *

# 메뉴얼 App 각 페이지의 Admin 정의

@admin.register(CompareWord)
class CompareWordAdmin(admin.ModelAdmin):
    list_display=['id', 'result', 'date']

@admin.register(WordDict)
class CompareWordAdmin(admin.ModelAdmin):
    list_display=['id', 'word', 'word_type', 'desc']