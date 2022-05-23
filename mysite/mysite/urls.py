from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from news.views import *   # импортирует все, import all

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
]

# На этапе разработки необходимо место для загрузки файлов/картинок
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                   ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
