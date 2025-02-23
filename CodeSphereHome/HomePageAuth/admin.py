from django.contrib import admin
from .models import User, Role, Profile, LoginHistory, PasswordReset

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active')
    search_fields = ('email',)

admin.site.register(Profile)
admin.site.register(LoginHistory)
admin.site.register(PasswordReset)
