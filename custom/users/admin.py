from django.contrib import admin
from .models import CustomUser

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'email', 'name', 'userType')
#     list_display_links = ('id', 'email')
#     list_editable = ('name', 'userType')
#     search_fields = ('name', 'userType', 'email')
#     list_per_page = 20

# admin.site.register(CustomUser, UserAdmin)
admin.site.register(CustomUser)