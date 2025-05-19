from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users.views import CustomLoginView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve


urlpatterns = ([
    path('', CustomLoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('forum/', include('forum.urls')),
    path('tickets/', include('tickets.urls')),
    path('users/', include('users.urls')),  # Добавили эту строку для лк
    path('meters/', include('meters.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)