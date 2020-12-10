from django.contrib import admin

from .models import Author, Category, Post, Tag

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Tag) 

admin.site.disable_action('delete_selected')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  exclude = ('creator', 'author', 'seen_count')

