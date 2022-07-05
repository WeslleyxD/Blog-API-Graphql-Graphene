from django.contrib import admin
from .models import Post, Comment

# https://docs.djangoproject.com/en/4.0/ref/contrib/admin/


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status', 'tag')
    list_filter = ('status', 'created_date', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'publish','created_date', 'active')
    list_filter = ('active', 'created_date', 'updated_date')
    search_fields = ('name', 'email', 'body')
