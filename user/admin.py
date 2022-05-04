from pyexpat import model
from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('first_name', 'last_name', 'email', 'is_staff', 'is_active', 'is_superuser', 'date_joined', 'last_login', 'email_confirmed')
    list_editable = ('email_confirmed',)
    list_display_links = ('first_name', 'last_name', 'email')
    fieldsets = (
        (None, {
            "fields": (
                'email',
                'first_name',
                'last_name',
            ),
        }),
    )
    
    search_fields = ('email',)
    ordering = ('-date_joined',)


admin.site.register(CustomUser, CustomUserAdmin)
