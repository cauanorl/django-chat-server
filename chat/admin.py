from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    ...


@admin.register(models.MessageTextType)
class TextMessageAdmin(admin.ModelAdmin):
    ...
