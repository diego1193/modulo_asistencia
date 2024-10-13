from django import forms
from .models import Asistencia, Estudiante


class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ["estudiante", "fecha", "estado_asistencia"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "estudiante": forms.Select(attrs={"class": "form-control"}),
            "estado_asistencia": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        curso = kwargs.pop("curso", None)
        super().__init__(*args, **kwargs)
        if curso:
            self.fields["estudiante"].queryset = Estudiante.objects.filter(curso=curso)

    def clean(self):
        cleaned_data = super().clean()
        estudiante = cleaned_data.get("estudiante")
        fecha = cleaned_data.get("fecha")

        if Asistencia.objects.filter(estudiante=estudiante, fecha=fecha).exists():
            raise forms.ValidationError(
                "Ya existe un registro de asistencia para este estudiante "
                "en esta fecha en el mismo curso."
            )
        return cleaned_data
