from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Coordinator

# Register CustomUser model with the admin interface
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'company', 'email_verified', 'is_staff']
    list_filter = ['is_staff', 'email_verified', 'company']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['username']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'email', 'company', 'address', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone_number', 'company', 'address', 'profile_picture', 'is_active', 'is_staff'),
        }),
    )

# Register CustomUser with the admin site
admin.site.register(CustomUser, CustomUserAdmin)

# Register Coordinator model
class CoordinatorAdmin(admin.ModelAdmin):
    list_display = ['user', 'user__username']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    
admin.site.register(Coordinator, CoordinatorAdmin)
