from django.contrib import admin

from .models import (
    UserLink,
)

@admin.register(UserLink)
class UserLinkAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'link_type', 'updated_on', 'content_type', 'object_id',
    )
    search_fields = (
        'user', 'link_type', 'content_type', 'object_id',
    )
