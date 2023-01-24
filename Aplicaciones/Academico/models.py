from django.db import models
from datetime import datetime
from .choices import *
# Create your models here.


class TipoUsuario(models.Model):
    # id = models.PositiveIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self) -> str:
        return "{}".format(self.nombre)

    class Meta:
        verbose_name = 'TipoUsuario'
        verbose_name_plural = 'TiposUsuario'
        db_table = 'tipo_usuario'


class Usuario(models.Model):
    # id = models.PositiveIntegerField(primary_key=True)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    tipo_usuario = models.ForeignKey(
        TipoUsuario, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "{}, {}".format(self.login, self.tipo_usuario)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'usuario'
        ordering = ['login']


class Area(models.Model):
    # id = models.PositiveIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self) -> str:
        return "{}".format(self.nombre)

    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'
        db_table = 'area'
        ordering = ['nombre']


class Docente(models.Model):
    identificacion = models.PositiveIntegerField(primary_key=True)
    nombres = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=20)
    apellido_materno = models.CharField(max_length=20)
    tipo_identificacion = models.CharField(
        max_length=6, choices=tipoIdentificacion, default='CC')
    tipo_docente = models.CharField(
        max_length=11, choices=tipoDocente, default='Tecnico')
    tipo_contrato = models.CharField(
        max_length=11, choices=tipoContrato, default='PT')
    area = models.ForeignKey(
        Area, null=True, blank=True, on_delete=models.CASCADE)

    def nombre_completo(self):
        return "{} {}, {}".format(self.apellido_paterno, self.apellido_materno, self.nombres)

    def __str__(self) -> str:
        return self.nombre_completo()

    class Meta:
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'
        db_table = 'docente'
        ordering = ['apellido_paterno', '-apellido_materno']


class Ambiente(models.Model):
    codigo = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=50)
    tipo_ambiente = models.CharField(
        max_length=11, choices=tipoAmbiente, default='V')
    capacidad = models.PositiveIntegerField()
    ubicacion = models.CharField(max_length=50)

    def __str__(self) -> str:
        return "{}, {}".format(self.nombre, self.tipo_ambiente)

    class Meta:
        verbose_name = 'Ambiente'
        verbose_name_plural = 'Ambientes'
        db_table = 'ambiente'


class Programa(models.Model):
    # id = models.PositiveIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    # competencias = models.ManyToManyField(Competencia)

    def __str__(self) -> str:
        return "{}".format(self.nombre)

    class Meta:
        verbose_name = 'Programa'
        verbose_name_plural = 'Programas'
        db_table = 'programa'


class Competencia(models.Model):
    # id = models.PositiveIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    tipo_competencia = models.CharField(
        max_length=1, choices=tipoCompetencia, default='G')
    programa = models.ForeignKey(
        Programa, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "{}".format(self.nombre)

    class Meta:
        verbose_name = 'Competencia'
        verbose_name_plural = 'Competencias'
        db_table = 'competencia'


class PeriodoAcademico(models.Model):
    # id = models.PositiveIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    fecha_inicial = models.DateField()
    fecha_final = models.DateField()
    programas = models.ManyToManyField(Programa)

    def __str__(self) -> str:
        return "{}".format(self.nombre)

    class Meta:
        verbose_name = 'PeriodoAcademico'
        verbose_name_plural = 'PeriodosAcademicos'
        db_table = 'periodo_academico'


class FranjaHoraria(models.Model):
    # id = models.PositiveIntegerField(primary_key=True)
    # competencia = models.ForeignKey(Competencia, null=True, blank=True, on_delete=models.CASCADE)
    dia = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    horas_dia = models.PositiveIntegerField(editable=False)

    def save(self, *args, **kwargs):
        start_time = datetime.combine(self.dia, self.hora_inicio)
        end_time = datetime.combine(self.dia, self.hora_fin)
        delta = end_time - start_time
        self.horas_dia = delta.seconds // 3600
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return "{} - {} horas".format(self.dia, self.horas_dia)

    class Meta:
        verbose_name = 'FranjaHoraria'
        verbose_name_plural = 'FranjasHorarias'
        db_table = 'franja_horaria'


class Horario(models.Model):
    # id = models.PositiveIntegerField(primary_key=True)
    periodo = models.ForeignKey(
        PeriodoAcademico, null=True, blank=True, on_delete=models.CASCADE)
    docente = models.ForeignKey(
        Docente, null=True, blank=True, on_delete=models.CASCADE)
    f_horaria = models.ForeignKey(
        FranjaHoraria, null=True, blank=True, on_delete=models.CASCADE)
    competencia = models.ForeignKey(
        Competencia, null=True, blank=True, on_delete=models.CASCADE)
    ambiente = models.ForeignKey(
        Ambiente, null=True, blank=True, on_delete=models.CASCADE)
    horas_sem = models.PositiveIntegerField()

    def __str__(self) -> str:
        return "{}, {}, {}, {}, {}".format(self.periodo, self.docente, self.f_horaria, self.ambiente, self.horas_sem)

    class Meta:
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
        db_table = 'horario'
