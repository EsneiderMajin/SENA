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
    path('gestionAmbientes/registrarAmbiente/', login_required(views.registrarAmbiente)),
    path('gestionAmbientes/editarAmbiente/<codigo>', login_required(views.editarAmbiente)),
    path('gestionAmbientes/edicionAmbiente/', login_required(views.edicionAmbiente)),
    path('gestionAmbientes/eliminarAmbiente/<codigo>', login_required(views.eliminarAmbiente)),
    #Periodos
    path('gestionPeriodos/', login_required(views.gestionPeriodos)),
    path('gestionPeriodos/registrarPeriodo/', login_required(views.registrarPeriodo)),
    path('gestionPeriodos/editarPeriodo/<id>', login_required(views.editarPeriodo)),
    path('gestionPeriodos/edicionPeriodo/', login_required(views.edicionPeriodo)),
    path('gestionPeriodos/eliminarPeriodo/<id>', login_required(views.eliminarPeriodo)),
    #Programas
    path('gestionProgramas/', login_required(views.gestionProgramas)),
    path('gestionProgramas/registrarPrograma/', login_required(views.registrarPrograma)),
    path('gestionProgramas/editarPrograma/<id>', login_required(views.editarPrograma)),
    path('gestionProgramas/edicionPrograma/', login_required(views.edicionPrograma)),
    path('gestionProgramas/eliminarPrograma/<id>', login_required(views.eliminarPrograma)),
    #Competencias
    path('gestionCompetencias/', login_required(views.gestionCompetencias)),
    path('gestionCompetencias/registrarCompetencia/', login_required(views.registrarCompetencia)),
    path('gestionCompetencias/editarCompetencia/<id>', login_required(views.editarCompetencia)),
    path('gestionCompetencias/edicionCompetencia/', login_required(views.edicionCompetencia)),
    path('gestionCompetencias/eliminarCompetencia/<id>', login_required(views.eliminarCompetencia)),

    #Sesion
    path('login/', views.login)
]
