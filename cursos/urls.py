from django.urls import path
from .views import CursoDetailView, CursoList

cursos_patterns = (
    [
        path("", CursoList.as_view(), name="cursos"),
        path(
            "<str:codigo_curso>/estudiantes/",
            CursoDetailView.as_view(),
            name="curso",
        ),
    ],
    "cursos",
)
