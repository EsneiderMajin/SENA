# Generated by Django 3.2.13 on 2023-01-25 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academico', '0008_remove_horario_horas_sem'),
    ]

    operations = [
        migrations.AddField(
            model_name='ambiente',
            name='estado',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='docente',
            name='estado',
            field=models.BooleanField(default=True),
        ),
    ]
