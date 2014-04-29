from django.contrib import admin

from monitor import models


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_created', 'last_updated', 'hostname')
    search_fields = ('name', 'hostname', 'description')

admin.site.register(models.Module, ModuleAdmin)
# Register your models here.