from django.contrib import admin

from .models import Abonent


class AbonentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'phone',
        'username',
    )
    search_fields = ('username', 'phone')
    empty_value_display = '-пусто-'


admin.site.register(Abonent, AbonentAdmin)
