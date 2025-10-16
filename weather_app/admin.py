from django.contrib import admin
from .models import City

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'last_temperature', 'last_description', 'searched_at')
    search_fields = ('name', 'country')
    list_filter = ('country',)
    ordering = ('-searched_at',)
