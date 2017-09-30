from django.contrib import admin
from .models import Post, PostComments
from django.contrib.admin import ListFilter, FieldListFilter

# Register your models here.
# admin.site.register(Post)
# admin.site.register(User)
admin.site.register(PostComments)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('id', 'author', 'title', 'text', 'publish_time','picture')
