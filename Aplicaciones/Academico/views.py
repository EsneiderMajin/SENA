from django.shortcuts import render, redirect
from .models import*
from django.contrib import messages
# Create your views here.

#Inicio
def home(request):
    return render(request, "index.html")

def return_home(request):
    return redirect('/')

#Horarios
def gestionHorarios(request):
    return render(request, "gestion-horarios.html")

#Docentes
def gestionDocentes(request):
    docentesListados = Docente.objects.all()
    return render(request, "gestion-docentes.html", {"docentes": docentesListados})

#Ambientes
def gestionAmbientes(request):
    ambientesListados = Ambiente.objects.all()
    return render(request, "gestion-ambientes.html", {"ambientes": ambientesListados})

def registrarAmbiente(request):
    #Recuperar los datos del form html
    codigo = request.POST['txtCodigo']
    nombre = request.POST['txtNombre']
    tipo_ambiente =  request.POST['tipoAmbiente']
    capacidad = request.POST['txtCapacidad']
    ubicacion = request.POST['txtUbicacion']
    #Registrar
    ambiente = Ambiente.objects.create(codigo=codigo, nombre=nombre, tipo_ambiente=tipo_ambiente, capacidad=capacidad, ubicacion=ubicacion)
    messages.success(request, '¡Ambiente registrado!')
    #Recargar la página
    return redirect('/gestionAmbientes/')

def editarAmbiente(request, codigo):
    ambiente = Ambiente.objects.get(codigo=codigo)
    return render(request, "edicion-ambiente.html", {'ambiente':ambiente})

def edicionAmbiente(request):
    codigo = request.POST['txtCodigo']
    nombre = request.POST['txtNombre']
    tipo_ambiente =  request.POST['tipoAmbiente']
    capacidad = request.POST['txtCapacidad']
    ubicacion = request.POST['txtUbicacion']

    ambiente = Ambiente.objects.get(codigo=codigo)
    ambiente.nombre = nombre
    ambiente.tipo_ambiente = tipo_ambiente
    ambiente.capacidad = capacidad
    ambiente.ubicacion = ubicacion
    ambiente.save()

    messages.success(request, '¡Ambiente actualizado!')

    return redirect('/gestionAmbientes/')

def eliminarAmbiente(request, codigo):
    ambiente = Ambiente.objects.get(codigo=codigo)
    ambiente.delete()

    messages.success(request, '¡Ambiente eliminado!')

    return redirect('/gestionAmbientes/')

#Periodos
def gestionPeriodos(request):
    periodosListados = PeriodoAcademico.objects.all()
    #programasListados = Programa.objects.all()
    return render(request, "gestion-periodos.html", {"periodos": periodosListados})

def registrarPeriodo(request):
    #Recuperar los datos del form html
    id = request.POST['txtID']
    nombre = request.POST['txtNombre']
    fecha_inicial = request.POST['fechaInicial'] 
    fecha_final = request.POST['fechaFinal']
    #Registrar
    periodo = PeriodoAcademico.objects.create(id=id, nombre=nombre, fecha_inicial=fecha_inicial, fecha_final=fecha_final)
    messages.success(request, '¡Periodo registrado!')
    #Recargar la página
    return redirect('/gestionPeriodos/')

def editarPeriodo(request, id):
    periodo = PeriodoAcademico.objects.get(id=id)
    return render(request, "edicion-periodo.html", {'periodo': periodo})

def edicionPeriodo(request):
    id=request.POST['txtID']
    nombre=request.POST['txtNombre']
    fecha_incial = request.POST['fechaInicial'] 
    fecha_final = request.POST['fechaFinal']

    periodo = PeriodoAcademico.objects.get(id=id)
    periodo.nombre = nombre
    periodo.fecha_inicial= fecha_incial
    periodo.fecha_final = fecha_final
    periodo.save()

    messages.success(request, '¡Periodo actualizado!')

    return redirect('/gestionPeriodos/')

def eliminarPeriodo(request, id):
    periodo = PeriodoAcademico.objects.get(id=id)
    periodo.delete()

    messages.success(request, '¡Periodo eliminado!')

    return redirect('/gestionPeriodos/')

#Programas
def gestionProgramas(request):
    programasListados = Programa.objects.all()
    return render(request, "gestion-programas.html", {"programas": programasListados})

def registrarPrograma(request):
    #Recuperar los datos del form html
    id = request.POST['txtID']
    nombre = request.POST['txtNombre']
    #Registrar
    programa = Programa.objects.create(id=id, nombre=nombre)
    messages.success(request, '¡Programa registrado!')
    #Recargar la página
    return redirect('/gestionProgramas/')

def editarPrograma(request, id):
    programa = Programa.objects.get(id=id)
    return render(request, "edicion-programa.html", {'programa':programa})

def edicionPrograma(request):
    id=request.POST['txtID']
    nombre=request.POST['txtNombre']

    programa = Programa.objects.get(id=id)
    programa.nombre = nombre
    programa.save()

    messages.success(request, '¡Programa actualizado!')

    return redirect('/gestionProgramas/')

def eliminarPrograma(request, id):
    programa = Programa.objects.get(id=id)
    programa.delete()

    messages.success(request, '¡Programa eliminado!')

    return redirect('/gestionProgramas/')

#Competencias
def gestionCompetencias(request):
    competenciasListadas = Competencia.objects.all()
    return render(request, "gestion-competencias.html", {"competencias": competenciasListadas})

def registrarCompetencia(request):
    #Recuperar los datos del form html
    id = request.POST['txtID']
    nombre = request.POST['txtNombre']
    tipo_competencia = request.POST['tipoCompetencia']
    #Registrar
    competencia = Competencia.objects.create(id=id, nombre=nombre, tipo_competencia = tipo_competencia)
    # messages.success(request, '¡Estudiante registrado!')
    #Recargar la página
    return redirect('/gestionCompetencias/')

def editarCompetencia(request, id):
    competencia = Competencia.objects.get(id=id)
    return render(request, "edicion-competencia.html", {'competencia':competencia})

def edicionCompetencia(request):
    id=request.POST['txtID']
    nombre=request.POST['txtNombre']
    tipo_competencia = request.POST['tipoCompetencia']

    competencia = Competencia.objects.get(id=id)
    competencia.nombre = nombre
    competencia.tipo_competencia = tipo_competencia
    competencia.save()

    #messages.success(request, '¡Estudiante actualizado!')

    return redirect('/gestionCompetencias/')

def eliminarCompetencia(request, id):
    competencia = Competencia.objects.get(id=id)
    competencia.delete()

    #messages.success(request, '¡Estudiante eliminado!')

    return redirect('/gestionCompetencias/')

#Sesión
def login(request):
    return render(request, "login.html")
