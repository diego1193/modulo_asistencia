from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Curso, Estudiante, Asistencia
from datetime import date, timedelta


class CursoDetailViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.curso = Curso.objects.create(
            codigo_curso="CS101", nombre_curso="Ciencia de Datos"
        )
        self.estudiante = Estudiante.objects.create(
            id_estudiante="E001", nombre="Juan Pérez", curso=self.curso
        )
        # Usamos una fecha inicial de asistencia
        self.asistencia = Asistencia.objects.create(
            estudiante=self.estudiante,
            fecha=date.today(),
            estado_asistencia="P",
        )
        self.url = reverse(
            "cursos:curso", kwargs={"codigo_curso": self.curso.codigo_curso}
        )

    def test_acceso_sin_autenticacion(self):
        # Verifica que la vista requiera autenticación
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"/asistencia/login/?next={self.url}")

    def test_acceso_con_autenticacion(self):
        # Verifica que un usuario autenticado pueda acceder a la vista
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cursos/curso_detail.html")

    def test_filtro_por_nombre_estudiante(self):
        # Verifica que el filtro de nombre del estudiante funcione
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url, {"q": "Juan"})
        self.assertContains(response, "Juan Pérez")

    def test_filtro_por_fecha(self):
        # Verifica que el filtro por fecha funcione
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url, {"date": date.today().isoformat()})
        self.assertContains(response, str(date.today()))

    def test_filtro_por_estado(self):
        # Verifica que el filtro por estado funcione
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url, {"estado": "P"})
        self.assertContains(response, "Presente")

    def test_creacion_asistencia(self):
        # Verifica que una nueva asistencia se pueda crear con una fecha distinta
        self.client.login(username="testuser", password="testpass")
        nueva_fecha = date.today() + timedelta(days=1)
        data = {
            "estudiante": self.estudiante.id,
            "fecha": nueva_fecha.isoformat(),
            "estado_asistencia": "A",
        }
        response = self.client.post(self.url, data)

        self.assertEqual(
            response.status_code,
            302,
            msg=f"Respuesta: {response.status_code}, contenido: {response.content}",
        )

        # Verifica que la asistencia fue creada
        asistencia_creada = Asistencia.objects.filter(
            estudiante=self.estudiante, fecha=nueva_fecha, estado_asistencia="A"
        ).exists()
        self.assertTrue(
            asistencia_creada,
            msg=f"Asistencia no encontrada: {Asistencia.objects.all()}",
        )

    def test_creacion_asistencia_duplicada(self):
        # Verifica que no se permita la creación de duplicados
        self.client.login(username="testuser", password="testpass")
        data = {
            "estudiante": self.estudiante.id,
            "fecha": self.asistencia.fecha.isoformat(),
            "estado_asistencia": "A",
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)

        # Verifica que el formulario contenga el error de validación esperado
        self.assertContains(
            response,
            "Ya existe un registro de asistencia para este estudiante "
            "en esta fecha en el mismo curso.",
        )
