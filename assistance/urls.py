from django.contrib import admin
from django.urls import path, include
from cursos.urls import cursos_patterns
from core.urls import core_patterns
from django.views.generic import RedirectView

from django.conf import settings

urlpatterns = [
    path("asistencia/", include(core_patterns)),
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("asistencia/cursos/", include(cursos_patterns)),
    path("", RedirectView.as_view(url="/asistencia/login/", permanent=True)),
]


if settings.DEBUG is True:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
