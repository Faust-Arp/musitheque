from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from account.views import signup
from musitheque import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('library/', include('library.urls')),
    path('compte/', include('django.contrib.auth.urls')),
    path('compte/nouveau', signup, name="signup"),
    path('statistic/', include('statistic.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)