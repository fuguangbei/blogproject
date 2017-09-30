from django.contrib import admin
from .models import Sensitive,Feedback
# Register your models here.
admin.site.register(Sensitive)
# admin.site.register(Feedback)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
	list_display = ('id', 'text', 'feed_time', 'solute_time', 'is_solved')