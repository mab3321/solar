from django.contrib import admin
from .models import Business, Service, UserIntegration, Notification, Setting

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'industry', 'stage', 'user')
    search_fields = ('business_name', 'industry', 'stage', 'user__username')
    list_filter = ('industry', 'stage')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'type', 'resource', 'status', 'created_at', 'updated_at')
    search_fields = ('name', 'category', 'type', 'status')
    list_filter = ('category', 'status')

@admin.register(UserIntegration)
class UserIntegrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'status', 'business_id', 'created_at', 'updated_at')
    search_fields = ('user__username', 'service__name', 'status')
    list_filter = ('status',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'time', 'read_at', 'type', 'from_user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'subject', 'type', 'from_user')
    list_filter = ('type', 'read_at')

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_id', 'name', 'type', 'value', 'created_at', 'updated_at')
    search_fields = ('user__username', 'name', 'type', 'value')
    list_filter = ('type',)
