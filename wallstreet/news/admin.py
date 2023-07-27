from django.contrib import admin
from .models import News
from django.contrib.messages import constants as messages
# Register your models here.


@admin.action(description='Publish News')
def make_published(modeladmin, request, queryset):
    for q in queryset:
        q.publish()
    modeladmin.message_user(request, f"{len(queryset)} News Published.", messages.SUCCESS)

class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'isPublished']
    ordering = ['title']
    actions = [make_published]

admin.site.register(News, NewsAdmin)