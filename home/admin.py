from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from home.models import User


class UserAdmin(BaseUserAdmin):
  
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id','email', 'username','profile_picture','is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('username','email', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name','profile_picture')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name','last_name','username', 'profile_picture','password', 'password2'),
        }),
    )
    search_fields = ('username','email',)
    ordering = ('id','email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)