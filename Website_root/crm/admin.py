from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.forms import Media
from .models import User, Applications

class CustomUserAdmin(UserAdmin):
    list_display_links = ['first_name', 'last_name','email']
    list_display = ['first_name', 'last_name', 'email', 'phone', 'user_applications']
    search_fields = ['first_name', 'last_name', 'email', 'phone']

    def user_applications(self, obj):
        return obj.get_user_applications().count()

    user_applications.short_description = 'Wnioski użytkownika'

    fieldsets = (
        (None, {'fields': ()}),
        ('Informacja osobista', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Czas korzystania', {'fields': ('last_login', 'date_joined')}),
        ('Uprawnienia i grupy', {'fields': ('is_active', 'is_staff', 'is_superuser', "groups")}),
    )

class ApplicationsAdmin(admin.ModelAdmin):
    list_display = ['completed','from_who', 'desired_appointment_date', 'date_created', 'mark', 'model']
    search_fields = ['vin_code', 'reg_num', 'mark', 'model', 'desired_appointment_date']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Applications, ApplicationsAdmin)

admin.site.site_header = 'Administracja Nikoserwis'
