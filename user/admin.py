from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
# Register your models here.

@admin.register(User)
class UsersAdmin(ImportExportModelAdmin):
    list_display = ('email', 'phone_number', 'is_admin', 'is_farmer', 'is_agric_enterprise', 'is_customer')
    search_fields = ['username', 'first_name', 'last_name']
    list_filter = ('is_admin', 'is_farmer', 'is_agric_enterprise', 'is_customer')

@admin.register(Profile)
class UsersAdmin(ImportExportModelAdmin):
    list_display = ('user', 'bio','created_at',)
    list_filter = ('created_at',)
    search_fields = ['user',]
    

# @admin.register(PhoneNumber)
# class PhoneNumberAdmin(ImportExportModelAdmin):
#     list_display = ('user', 'phone_number', 'security_code', 'is_verified', 'sent')

admin.site.site_header = "GreenPurseBackEnd Administration Dashboard"
