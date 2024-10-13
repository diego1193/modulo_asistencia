from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Curso, Asistencia
from .forms import AsistenciaForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@method_decorator(login_required, name="dispatch")
class CursoList(ListView):
    model = Curso
    template_name = "cursos/curso_list.html"


@method_decorator(login_required, name="dispatch")
class CursoDetailView(DetailView):
    model = Curso
    template_name = "cursos/curso_detail.html"
    context_object_name = "curso"

    def get_object(self):
        codigo_curso = self.kwargs["codigo_curso"]
        return get_object_or_404(Curso, codigo_curso=codigo_curso)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filtros de búsqueda
        search_query = self.request.GET.get("q", "")
        date_filter = self.request.GET.get("date", "")
        estado_filter = self.request.GET.get("estado", "")

        asistencias = Asistencia.objects.filter(estudiante__curso=self.object)

        if search_query:
            asistencias = asistencias.filter(estudiante__nombre__icontains=search_query)
        if date_filter:
            asistencias = asistencias.filter(fecha=date_filter)
        if estado_filter:
            asistencias = asistencias.filter(estado_asistencia=estado_filter)

        paginator = Paginator(asistencias, 10)
        page = self.request.GET.get("page")
        try:
            asistencias_paginadas = paginator.page(page)
        except PageNotAnInteger:
            asistencias_paginadas = paginator.page(1)
        except EmptyPage:
            asistencias_paginadas = paginator.page(paginator.num_pages)

        context["asistencias"] = asistencias_paginadas
        context["form"] = AsistenciaForm(curso=self.object)
        context["paginator"] = paginator

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        asistencia_id = request.POST.get("asistencia_id")
        if asistencia_id:
            # Proceso de actualización
            asistencia = get_object_or_404(Asistencia, id=asistencia_id)
            estado_asistencia = request.POST.get("estado_asistencia")
            asistencia.estado_asistencia = estado_asistencia
            asistencia.save()
            messages.success(request, "Estado de asistencia actualizado exitosamente.")
            return redirect(request.path)

        # Proceso de creación de nueva asistencia
        form = AsistenciaForm(request.POST, curso=self.object)
        if form.is_valid():
            form.save()
            messages.success(request, "Asistencia registrada exitosamente.")
            return redirect(request.path)
        else:
            context = self.get_context_data(object=self.object)
            context["form"] = form
            return self.render_to_response(context)
