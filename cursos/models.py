from django.db import models


class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Curso(Base):
    codigo_curso = models.CharField(max_length=20, unique=True)
    nombre_curso = models.CharField(max_length=100)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return self.nombre_curso


class Estudiante(Base):
    id_estudiante = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="estudiantes")

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["created"]


class Asistencia(Base):

    ESTADO_CHOICES = [("P", "Presente"), ("A", "Ausente")]

    estudiante = models.ForeignKey(
        Estudiante, on_delete=models.CASCADE, related_name="asistencias"
    )
    fecha = models.DateField()
    estado_asistencia = models.CharField(max_length=1, choices=ESTADO_CHOICES)

    def __str__(self):
        return (
            f"{self.estudiante.nombre} - {self.created} - "
            f"{self.get_estado_asistencia_display()}"
        )

    class Meta:
        ordering = ["fecha"]
