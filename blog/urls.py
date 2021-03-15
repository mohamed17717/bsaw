from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from posts.views import (
    index,
    post,
    create_post,
    listPosts,
    static_template
)

from django.contrib.sitemaps.views import sitemap
from posts.sitemaps import Static_Sitemap
from posts.sitemaps import Post_Sitemap

from django.views.generic.base import TemplateView


sitemaps = {
    'article': Post_Sitemap(),
    'static': Static_Sitemap(),
}

urlpatterns = [
    # home
    path('', index, name='home'),
    # post detail
    path('post/<int:pk>/', post, name="post-detail"),
    # lists
    path('search/<str:query>/', listPosts('search_posts'), name='search'),
    path('category/<str:title>/', listPosts('category_posts'), name='category-filter'),
    path('tag/<str:title>/', listPosts('tag_posts'), name='tag-filter'),
    path('latest/posts/', listPosts('latest_posts'), name='latest-posts'),

    # static urls
    path('privacy-policy/', static_template('privacy.html'), name='privacy-policy'),
    path('about-us/', static_template('aboutus.html'), name='about-us'),
    path('contact-us/', static_template('contactus.html'), name='contact-us'),

    # create from the collector
    path('create/post/', create_post, name='create-post'),

    # third party
    path('jJYDbuc44KAYpqiasHvI2HaPrut7B9/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    # SEO
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
