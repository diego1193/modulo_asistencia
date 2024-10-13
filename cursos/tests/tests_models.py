# core/tests.py
from django.test import TestCase
from ..models import Curso, Estudiante, Asistencia
from datetime import date


class CursoModelTest(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(
            codigo_curso="CS101", nombre_curso="Ciencia de Datos"
        )

    def test_curso_str(self):
        self.assertEqual(str(self.curso), "Ciencia de Datos")


class EstudianteModelTest(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(
            codigo_curso="CS101", nombre_curso="Ciencia de Datos"
        )
        self.estudiante = Estudiante.objects.create(
            id_estudiante="E001", nombre="Juan Pérez", curso=self.curso
        )

    def test_estudiante_str(self):
        self.assertEqual(str(self.estudiante), "Juan Pérez")

    def test_estudiante_curso(self):
        self.assertEqual(self.estudiante.curso.nombre_curso, "Ciencia de Datos")


class AsistenciaModelTest(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(
            codigo_curso="CS101", nombre_curso="Ciencia de Datos"
        )
        self.estudiante = Estudiante.objects.create(
            id_estudiante="E001", nombre="Juan Pérez", curso=self.curso
        )
        self.asistencia = Asistencia.objects.create(
            estudiante=self.estudiante,
            fecha=date.today(),
            estado_asistencia="P",
        )

    def test_asistencia_str(self):
        expected_str = f"{self.estudiante.nombre} - {self.asistencia.created} - Presente"
        self.assertEqual(str(self.asistencia), expected_str)

    def test_asistencia_estado(self):
        self.assertEqual(self.asistencia.estado_asistencia, "P")
        self.assertEqual(self.asistencia.get_estado_asistencia_display(), "Presente")
