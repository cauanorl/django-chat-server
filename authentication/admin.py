from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ['id']
