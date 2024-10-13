from django.contrib import admin
from .models import Estudiante, Curso, Asistencia


class AsistenciaInline(admin.TabularInline):
    model = Asistencia
    fields = ["fecha", "estado_asistencia"]
    can_delete = True
    extra = 1


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "updated")

    class Meta:
        abstract = True


class CursoAdmin(BaseAdmin):
    list_display = ("nombre_curso", "codigo_curso")


class EstudianteAdmin(BaseAdmin):
    list_display = ("nombre", "curso")
    inlines = [AsistenciaInline]


admin.site.register(Curso, CursoAdmin)
admin.site.register(Estudiante, EstudianteAdmin)
