from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Recommendation for converted strings in Python to human readable text
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    # Order by Id
    ordering = ['id']
    # Display only email and name
    list_display = ['email', 'name']

    # User fields that admin is allowed to change 
    fieldsets = (
        # (title for the section, fields )
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {   'fields': (
                    'is_active', 
                    'is_staff', 
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    
    # support creating new users
    add_fieldsets = (
        (None, {
            'classes' : ('wide', ),
            'fields' : ('email', 'password1', 'password2')
        }),
    )

# register UserAdmin class to that model
admin.site.register(models.User, UserAdmin)
