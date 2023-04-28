from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Purchase

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Information', {
            'fields': ('full_name', 'phone_number', 'address', 'bank_account_details', 'referrer','referral_code','balance'),
        }),
    )
    readonly_fields = ('referral_code',)
    list_display = ('username', 'full_name', 'referrer','phone_number', 'balance', 'is_staff', 'is_active',)
    list_editable = ('balance',)

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Purchase)
