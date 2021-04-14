from django.contrib import admin

from .models import Author, Category, Post, Tag, Twt

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Tag) 

admin.site.disable_action('delete_selected')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  exclude = ('creator', 'author', 'seen_count')


@admin.register(Twt)
class TwtAdmin(admin.ModelAdmin):
  list_display = ('__str__',)
  actions = ['download_csv']

  def has_add_permission(self, request, obj=None):
    return False

  # This will help you to disable delete functionaliyt
  def has_delete_permission(self, request, obj=None):
    return False

  # This will help you to disable change functionality
  def has_change_permission(self, request, obj=None):
    return False

  def download_csv(self, request, queryset):
    import csv
    from django.http import HttpResponse
    from io import StringIO

    f = StringIO()
    writer = csv.writer(f)
    writer.writerow(["data"])

    for s in queryset:
      writer.writerow([str(s)])

    f.seek(0)
    response = HttpResponse(f, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=stat-info.csv'
    return response