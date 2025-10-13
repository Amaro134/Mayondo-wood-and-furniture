from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Add_user, Sales, Stock

class AddUserAdmin(UserAdmin):
    model = Add_user
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),  # Add role field to admin
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

admin.site.register(Add_user, AddUserAdmin)
admin.site.register(Sales)
admin.site.register(Stock)
