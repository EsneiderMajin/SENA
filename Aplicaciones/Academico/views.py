from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from .forms import UserRegisterForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
from django.http import HttpResponse
from datetime import datetime, timedelta
import json
# Create your views here.

# Inicio
class Inicio(LoginRequiredMixin, TemplateView):

    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        usuario = get_user(request)
        if usuario.is_superuser:
            return render(request, self.template_name)
        else:
            return render(request, "inicio-docente.html")


def home(request):
    usuario = get_user(request)
    if usuario.is_superuser:
        return render(request, "index.html")
    else:
        return render(request, "inicio-docente.html")


def signup(request):
    if request.method == 'GET':
        return render(request, 'register.html', {
            'form': UserRegisterForm
        })
    else:
        docentesListados = Docente.objects.all()
        for docente in docentesListados:
            if request.POST['username'] == docente.nombres:
                usuario = True
            else:
                usuario = False
        if usuario:
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(username=request.POST['username'],
                                                    password=request.POST['password1'])
                    user.save()
                    messages.success(request, f'Usuario registrado!')
                    return redirect('/accounts/login/')
                except:
                    messages.error(request, f'Usuario ya existente!')
            else:
                messages.error(request, f'Las contraseñas no coinciden!')
        else:
            messages.error(request, f'El usuario no es valido!')
        return redirect('/accounts/login/signup')

def return_home(request):
    return redirect('/')

# Horarios
def gestionHorarios(request):
    periodosListados = PeriodoAcademico.objects.all()
    docentesListados = Docente.objects.all()
    franjasListadas = FranjaHoraria.objects.all()
    competenciasListadas = Competencia.objects.all()
    ambientesListados = Ambiente.objects.all()
    usuario = get_user(request)
    if usuario.is_superuser:

        return render(request, "gestion-horarios.html", {"docentes": docentesListados,
                                                         "periodos": periodosListados,
                                                         "franjas": franjasListadas,
                                                         "competencias": competenciasListadas,
                                                         "ambientes": ambientesListados, })
    else:
        horariosListados = Horario.objects.all()
        return render(request, "gestion-horario-docente.html",{"franjas": franjasListadas, "horarios": horariosListados})


def registrarHorario(request):
    # Recuperar los datos del form html
    docente_id = request.POST['docente']
    periodo_id = request.POST['periodo']
    franja_id = request.POST['franja']
    competencia_id = request.POST['competencia']
    ambiente_id = request.POST['ambiente']
    #Objects
    periodo = PeriodoAcademico.objects.get(id=periodo_id)
    docente = Docente.objects.get(identificacion=docente_id)
    franja = FranjaHoraria.objects.get(id=franja_id)
    competencia = Competencia.objects.get(id=competencia_id)
    ambiente = Ambiente.objects.get(codigo=ambiente_id)
    # Registrar
    Horario.objects.create(docente=docente, f_horaria=franja, ambiente=ambiente, periodo=periodo, competencia=competencia)
    messages.success(request, '¡Horario registrado!')
    # Recargar la página
    return redirect('/app/gestionHorarios/')

# Docentes
def gestionDocentes(request):
    usuario = get_user(request)
    if usuario.is_superuser:
        docentesListados = Docente.objects.all()
        return render(request, "gestion-docentes.html", {"docentes": docentesListados})
    else:
        return render(request, "denegado.html")


class DocenteView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, identificacion=0):
        if (identificacion > 0):
            docentes = list(Docente.objects.filter(
                identificacion=identificacion).values())
            if len(docentes) > 0:
                docente = docentes[0]
                datos = {'message': "Success", 'docente': docente}
            else:
                datos = {'message': "No se ha encontrado al docente"}
        else:
            docentes = list(Docente.objects.values())
            if len(docentes) > 0:
                datos = {'message': "Success", 'docentes': docentes}
            else:
                datos = {'message': "No se encontraron docentes"}
        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        # print(jd)
        area_id = Area.objects.get(id=jd['area_id'])
        Docente.objects.create(identificacion=jd['identificacion'],
                               nombres=jd['nombres'],
                               apellido_paterno=jd['apellido_paterno'],
                               apellido_materno=jd['apellido_materno'],
                               tipo_identificacion=jd['tipo_identificacion'],
                               tipo_docente=jd['tipo_docente'],
                               tipo_contrato=jd['tipo_contrato'],
                               area=area_id,
                               estado=jd['estado'])
        datos = {'message': "Success"}
        return JsonResponse(datos)

    def put(self, request, identificacion):
        jd = json.loads(request.body)
        area_id = Area.objects.get(id=jd['area_id'])
        docentes = list(Docente.objects.filter(
            identificacion=identificacion).values())
        if len(docentes) > 0:
            docente = Docente.objects.get(identificacion=identificacion)
            docente.identificacion = jd['identificacion']
            docente.nombres = jd['nombres']
            docente.apellido_paterno = jd['apellido_paterno']
            docente.apellido_materno = jd['apellido_materno']
            docente.tipo_identificacion = jd['tipo_identificacion']
            docente.tipo_docente = jd['tipo_docente']
            docente.tipo_contrato = jd['tipo_contrato']
            docente.area = area_id
            docente.estado = jd['estado']
            docente.save()
            datos = {'message': "Success"}
        else:
            datos = {'message': "No se ha encontrado al docente"}
        return JsonResponse(datos)

    def delete(self, request, identificacion):
        docentes = list(Docente.objects.filter(
            identificacion=identificacion).values())
        if len(docentes) > 0:
            Docente.objects.filter(identificacion=identificacion).delete()
            datos = {'message': "Success"}
        else:
            datos = {'message': "No se ha encontrado al docente"}
        return JsonResponse(datos)

# Ambientes
def gestionAmbientes(request):
    usuario = get_user(request)
    if usuario.is_superuser:
        ambientesListados = Ambiente.objects.all()
        return render(request, "gestion-ambientes.html", {"ambientes": ambientesListados})
    else:
        return render(request, "denegado.html")


def registrarAmbiente(request):
    # Recuperar los datos del form html
    codigo = request.POST['txtCodigo']
    nombre = request.POST['txtNombre']
    tipo_ambiente = request.POST['tipoAmbiente']
    capacidad = request.POST['txtCapacidad']
    ubicacion = request.POST['txtUbicacion']
    # Registrar
    ambiente = Ambiente.objects.create(
        codigo=codigo, nombre=nombre, tipo_ambiente=tipo_ambiente, capacidad=capacidad, ubicacion=ubicacion)
    messages.success(request, '¡Ambiente registrado!')
    # Recargar la página
    return redirect('/app/gestionAmbientes/')


def editarAmbiente(request, codigo):
    ambiente = Ambiente.objects.get(codigo=codigo)
    return render(request, "edicion-ambiente.html", {'ambiente': ambiente})


def edicionAmbiente(request):
    codigo = request.POST['txtCodigo']
    nombre = request.POST['txtNombre']
    tipo_ambiente = request.POST['tipoAmbiente']
    capacidad = request.POST['txtCapacidad']
    ubicacion = request.POST['txtUbicacion']

    ambiente = Ambiente.objects.get(codigo=codigo)
    ambiente.nombre = nombre
    ambiente.tipo_ambiente = tipo_ambiente
    ambiente.capacidad = capacidad
    ambiente.ubicacion = ubicacion
    ambiente.save()

    messages.success(request, '¡Ambiente actualizado!')
    return redirect('/app/gestionAmbientes/')


def eliminarAmbiente(request, codigo):
    ambiente = Ambiente.objects.get(codigo=codigo)
    ambiente.delete()

    messages.success(request, '¡Ambiente eliminado!')
    return redirect('/app/gestionAmbientes/')

def inactivarAmbiente(request, codigo):
    print(codigo)
    ambiente = Ambiente.objects.get(codigo=codigo)
    if ambiente.estado == True:
        print("Se ha inactivado")
        ambiente.estado = False
    elif ambiente.estado == False:
        ambiente.estado = True
        print("Se ha activado")
    ambiente.save()
    messages.success(request, '¡El estado del ambiente ha cambiado!')
    return redirect('/app/gestionAmbientes/')

# Periodos
def gestionPeriodos(request):
    usuario = get_user(request)
    if usuario.is_superuser:
        periodosListados = PeriodoAcademico.objects.all()
        return render(request, "gestion-periodos.html", {"periodos": periodosListados})
    else:
        return render(request, "denegado.html")


def registrarPeriodo(request):
    # Recuperar los datos del form html
    nombre = request.POST['txtNombre']
    fecha_inicial = datetime.strptime(request.POST['fechaInicial'], '%Y-%m-%d')
    fecha_final = datetime.strptime(request.POST['fechaFinal'], '%Y-%m-%d')
    if fecha_final - fecha_inicial < timedelta(days=90) or fecha_final - fecha_inicial > timedelta(days=180):
        messages.error(
            request, 'El rango entre la fecha inicial y final debe ser de 3 o 6 meses')
        return redirect('/app/gestionPeriodos/')
    # Registrar
    periodo = PeriodoAcademico.objects.create(
        nombre=nombre, fecha_inicial=fecha_inicial, fecha_final=fecha_final)
    messages.success(request, '¡Periodo registrado!')
    # Recargar la página
    return redirect('/app/gestionPeriodos/')


def editarPeriodo(request, id):
    periodo = PeriodoAcademico.objects.get(id=id)
    return render(request, "edicion-periodo.html", {'periodo': periodo})


def edicionPeriodo(request):
    id = request.POST['txtID']
    nombre = request.POST['txtNombre']
    fecha_incial = request.POST['fechaInicial']
    fecha_final = request.POST['fechaFinal']

    periodo = PeriodoAcademico.objects.get(id=id)
    periodo.nombre = nombre
    periodo.fecha_inicial = fecha_incial
    periodo.fecha_final = fecha_final
    periodo.save()

    messages.success(request, '¡Periodo actualizado!')
    return redirect('/app/gestionPeriodos/')


def eliminarPeriodo(request, id):
    periodo = PeriodoAcademico.objects.get(id=id)
    periodo.delete()

    messages.success(request, '¡Periodo eliminado!')
    return redirect('/app/gestionPeriodos/')

# Programas
def gestionProgramas(request):
    usuario = get_user(request)
    if usuario.is_superuser:
        programasListados = Programa.objects.all()
        return render(request, "gestion-programas.html", {"programas": programasListados})
    else:
        return render(request, "denegado.html")


def registrarPrograma(request):
    # Recuperar los datos del form html
    nombre = request.POST['txtNombre']
    # Registrar
    programa = Programa.objects.create(nombre=nombre)
    messages.success(request, '¡Programa registrado!')
    # Recargar la página
    return redirect('/app/gestionProgramas/')


def editarPrograma(request, id):
    programa = Programa.objects.get(id=id)
    return render(request, "edicion-programa.html", {'programa': programa})


def edicionPrograma(request):
    id = request.POST['txtID']
    nombre = request.POST['txtNombre']

    programa = Programa.objects.get(id=id)
    programa.nombre = nombre
    programa.save()

    messages.success(request, '¡Programa actualizado!')
    return redirect('/app/gestionProgramas/')


def eliminarPrograma(request, id):
    programa = Programa.objects.get(id=id)
    programa.delete()

    messages.success(request, '¡Programa eliminado!')
    return redirect('/app/gestionProgramas/')

# Competencias
def gestionCompetencias(request):
    usuario = get_user(request)
    if usuario.is_superuser:
        competenciasListadas = Competencia.objects.all()
        programasListados = Programa.objects.all()
        return render(request, "gestion-competencias.html", {"competencias": competenciasListadas, "programas": programasListados})
    else:
        return render(request, "denegado.html")


def registrarCompetencia(request):
    # Recuperar los datos del form html
    nombre = request.POST['txtNombre']
    tipo_competencia = request.POST['tipoCompetencia']
    programa_id = request.POST['programa']
    programa = Programa.objects.get(id=programa_id)
    print(programa_id)
    # Registrar
    competencia = Competencia.objects.create(
        nombre=nombre, tipo_competencia=tipo_competencia, programa=programa)

    messages.success(request, '¡Competencia registrada!')
    # Recargar la página
    return redirect('/app/gestionCompetencias/')


def editarCompetencia(request, id):
    competencia = Competencia.objects.get(id=id)
    programasListados = Programa.objects.all()
    return render(request, "edicion-competencia.html", {'competencia': competencia, "programas": programasListados})


def edicionCompetencia(request):
    id = request.POST['txtID']
    nombre = request.POST['txtNombre']
    tipo_competencia = request.POST['tipoCompetencia']
    programa_id = request.POST['programa']
    # print(programa_id)
    programa = Programa.objects.get(id=programa_id)
    competencia = Competencia.objects.get(id=id)
    competencia.nombre = nombre
    competencia.tipo_competencia = tipo_competencia
    competencia.programa = programa
    competencia.save()

    messages.success(request, '¡Competencia actualizada!')
    return redirect('/app/gestionCompetencias/')


def eliminarCompetencia(request, id):
    competencia = Competencia.objects.get(id=id)
    competencia.delete()

    messages.success(request, '¡Competencia eliminada!')
    return redirect('/app/gestionCompetencias/')

# Sesión
def login(request):
    return render(request, "login.html")
