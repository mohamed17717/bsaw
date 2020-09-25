from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from posts.views import index, blog, post, search, category_filter
from marketing.views import signup_newsletter

urlpatterns = [
    path('', index),
    path('blog/', blog, name="post-list"),
    path('post/<int:id>/', post, name="post-detail"),
    path('search/', search, name='search'),
    path('category/<str:title>/', category_filter, name='category-filter'),

    
    path('signup-newsletter/', signup_newsletter),
    path('admin/', admin.site.urls),

    path('tinymce/', include('tinymce.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
