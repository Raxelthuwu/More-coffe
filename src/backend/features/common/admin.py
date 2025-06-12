from django.contrib import admin
from .models import DjangoSession, DjangoMigrations, DjangoAdminLog, DjangoContentType

@admin.register(DjangoSession)
class DjangoSessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'expire_date')

@admin.register(DjangoMigrations)
class DjangoMigrationsAdmin(admin.ModelAdmin):
    list_display = ('app', 'name', 'applied')

@admin.register(DjangoContentType)
class DjangoContentTypeAdmin(admin.ModelAdmin):
    list_display = ('app_label', 'model')

@admin.register(DjangoAdminLog)
class DjangoAdminLogAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'object_repr', 'action_flag')
