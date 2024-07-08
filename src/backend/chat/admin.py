from django.contrib import admin

from . import models


@admin.register(models.ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "author_type", "notebook")
