from django.contrib import admin
from .models import Category, Tag, Post
# Register your models here.


class PostAdmin(admin.ModelAdmin):
	list_display = ['title', 'create_time', 'modify_time', 'category', 'author', 'id']


class CategoryAdmin(admin.ModelAdmin):
	list_display = ['id', 'name']


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)