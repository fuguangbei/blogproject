from django.contrib import admin
from models import *
admin.site.register(UserNotifications)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'triggering_user', 'action', 'content', 'receive_user', 'content_type', 'is_read')