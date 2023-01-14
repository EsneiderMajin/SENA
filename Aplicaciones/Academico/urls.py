from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from .views import DocenteView

urlpatterns = [
    #Principal
    path('', views.home),
    path('home/', views.return_home),
    #Horarios
    path('gestionHorarios/', login_required(views.gestionHorarios), name='gestion_horario'),
    #Docentes
    path('gestionDocentes/', login_required(views.gestionDocentes)),
    path('api/Docentes/', login_required(DocenteView.as_view()), name='docentes_list'),
    path('api/Docentes/<int:identificacion>', login_required(DocenteView.as_view()), name='docentes_process'),
    #Ambientes
    path('gestionAmbientes/', login_required(views.gestionAmbientes)),
    path('registrarAmbiente/', login_required(views.registrarAmbiente)),
    path('editarAmbiente/<codigo>', login_required(views.editarAmbiente)),
    path('edicionAmbiente/', login_required(views.edicionAmbiente)),
    path('eliminarAmbiente/<codigo>', login_required(views.eliminarAmbiente)),
    #Periodos
    path('gestionPeriodos/', login_required(views.gestionPeriodos)),
    path('registrarPeriodo/', login_required(views.registrarPeriodo)),
    path('editarPeriodo/<id>', login_required(views.editarPeriodo)),
    path('edicionPeriodo/', login_required(views.edicionPeriodo)),
    path('eliminarPeriodo/<id>', login_required(views.eliminarPeriodo)),
    #Programas
    path('gestionProgramas/', login_required(views.gestionProgramas)),
    path('registrarPrograma/', login_required(views.registrarPrograma)),
    path('editarPrograma/<id>', login_required(views.editarPrograma)),
    path('edicionPrograma/', login_required(views.edicionPrograma)),
    path('eliminarPrograma/<id>', login_required(views.eliminarPrograma)),
    #Competencias
    path('gestionCompetencias/', login_required(views.gestionCompetencias)),
    path('registrarCompetencia/', login_required(views.registrarCompetencia)),
    path('editarCompetencia/<id>', login_required(views.editarCompetencia)),
    path('edicionCompetencia/', login_required(views.edicionCompetencia)),
    path('eliminarCompetencia/<id>', login_required(views.eliminarCompetencia)),

    #Sesion
    path('login/', views.login)
]
