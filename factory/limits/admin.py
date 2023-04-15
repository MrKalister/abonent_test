from django.contrib import admin

from .models import Limit


class LimitAdmin(admin.ModelAdmin):
    list_display = (
        'order_id',
        'name',
        'description',
    )
    search_fields = ('name', 'description')
    empty_value_display = '-пусто-'


admin.site.register(Limit, LimitAdmin)
