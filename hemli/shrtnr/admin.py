from django.contrib import admin

from .models import ShortLink


class ShortLinkAdmin(admin.ModelAdmin):
    list_display = ['path', 'created_at', 'num_views', 'url']


admin.site.register(ShortLink, ShortLinkAdmin)
