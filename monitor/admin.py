from django.contrib import admin

from monitor import models


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_created', 'last_updated', 'hostname')
    search_fields = ('name', 'hostname', 'description')


class WatcherAdmin(admin.ModelAdmin):
    list_display = ('name', 'hostname', 'ip', 'port')
    ordering = ('name', 'hostname')
    search_fields = ('name', 'hostname', 'module', 'description')


class MonitorToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


admin.site.register(models.Module, ModuleAdmin)
admin.site.register(models.Watcher, WatcherAdmin)
admin.site.register(models.MonitorTool, MonitorToolAdmin)
# Register your models here.