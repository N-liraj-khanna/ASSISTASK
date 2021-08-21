from django.contrib import admin
from .models import Location
# Register your models here.

admin.site.site_header = "ADMIN DASHBOARD: Password Manager"

class AdminConfig(admin.ModelAdmin):
    list_display = ('website_name', 'author', 'created')
    exclude = ('website_password', 'master_password',)

admin.site.register(Location, AdminConfig)