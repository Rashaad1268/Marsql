from django.contrib import admin

from . import models


@admin.register(models.NoteBookDBConfig)
class NoteBookDBConfigAdmin(admin.ModelAdmin):
    list_display = ("id", "db_type")


@admin.register(models.NoteBook)
class NoteBookAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "creator", "db_config")


@admin.register(models.NoteBookCell)
class NoteBookCellAdmin(admin.ModelAdmin):
    list_display = ("id", "notebook", "type")
