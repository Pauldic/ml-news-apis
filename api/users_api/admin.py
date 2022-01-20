from django.contrib import admin
from .models import UserProfile


# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'first_name', 'last_name', 'address', 'country', 'liked', 'unliked', 'read', 'interests')
    list_filter = ('country', 'updated_at', 'created_at')


admin.site.register(UserProfile, UserProfileAdmin)
