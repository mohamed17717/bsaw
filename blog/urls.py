from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from posts.views import (
    index,
    post,
    create_post,
    listPosts,
)

urlpatterns = [
    path('', index),
    path('post/<int:id>/', post, name="post-detail"),

    path('search/<str:query>/', listPosts('search_posts'), name='search'),
    path('category/<str:title>/', listPosts('category_posts'), name='category-filter'),
    path('tag/<str:title>/', listPosts('tag_posts'), name='tag-filter'),
    path('latest/posts/', listPosts('latest_posts'), name='latest-posts'),

    path('create/post/', create_post, name='create-post'),

    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
