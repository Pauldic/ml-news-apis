from django.contrib import admin
from .models import News

# Register your models here.

class NewsAdmin(admin.ModelAdmin):
    list_display = ('link','source','author','title','description','category','url','urltoimage','publishedat','updatedat','entities','tags','liked','unliked')


admin.site.register(News,NewsAdmin)