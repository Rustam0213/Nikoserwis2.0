from django.contrib import admin
from .models import News, Promotion, Humor
from django.utils.safestring import mark_safe


class InfoAdminSettings(admin.ModelAdmin):
    list_display = ('header', 'date', 'get_img')

    def get_img(self, obj):
        if obj.img:
            return mark_safe(f'<img src="{obj.img.url}" width=80px/>')
        else:
            pass

admin.site.register(News,InfoAdminSettings)
admin.site.register(Promotion,InfoAdminSettings)
admin.site.register(Humor,InfoAdminSettings)