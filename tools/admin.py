from django.contrib import admin
from tools import models


class WatcherAdmin(admin.ModelAdmin):
    list_display = ('name', 'hostname', 'ip', 'port')
    ordering = ('name', 'hostname')
    search_fields = ('name', 'hostname', 'module', 'description')

admin.site.register(models.Watcher, WatcherAdmin)
# Register your models here.