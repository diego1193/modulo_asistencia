# Generated by Django 5.1.2 on 2024-10-11 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="estudiante",
            name="curso",
        ),
        migrations.DeleteModel(
            name="Asistencia",
        ),
        migrations.DeleteModel(
            name="Curso",
        ),
        migrations.DeleteModel(
            name="Estudiante",
        ),
    ]
