from django.contrib import admin

from tools import models


class WatcherAdmin(admin.ModelAdmin):
    list_display = ('name', 'hostname', 'ip', 'port')
    ordering = ('name', 'hostname')
    search_fields = ('name', 'hostname', 'module', 'description')


class MonitorToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

admin.site.register(models.Watcher, WatcherAdmin)
admin.site.register(models.MonitorTool, MonitorToolAdmin)
# Register your models here.