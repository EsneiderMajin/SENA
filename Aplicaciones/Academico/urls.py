from django.urls import path
from . import views
from .views import DocenteView

urlpatterns = [
    #Principal
    path('', views.home),
    path('home/', views.return_home),
    #Horarios
    path('gestionHorarios/', views.gestionHorarios),
    #Docentes
    path('gestionDocentes/', views.gestionDocentes),
    path('api/Docentes/', DocenteView.as_view(), name='docentes_list'),
    path('api/Docentes/<int:identificacion>', DocenteView.as_view(), name='docentes_process'),
    #Ambientes
    path('gestionAmbientes/', views.gestionAmbientes),
    path('registrarAmbiente/', views.registrarAmbiente),
    path('editarAmbiente/<codigo>', views.editarAmbiente),
    path('edicionAmbiente/', views.edicionAmbiente),
    path('eliminarAmbiente/<codigo>', views.eliminarAmbiente),
    #Periodos
    path('gestionPeriodos/', views.gestionPeriodos),
    path('registrarPeriodo/', views.registrarPeriodo),
    path('editarPeriodo/<id>', views.editarPeriodo),
    path('edicionPeriodo/', views.edicionPeriodo),
    path('eliminarPeriodo/<id>', views.eliminarPeriodo),
    #Programas
    path('gestionProgramas/', views.gestionProgramas),
    path('registrarPrograma/', views.registrarPrograma),
    path('editarPrograma/<id>', views.editarPrograma),
    path('edicionPrograma/', views.edicionPrograma),
    path('eliminarPrograma/<id>', views.eliminarPrograma),
    #Competencias
    path('gestionCompetencias/', views.gestionCompetencias),
    path('registrarCompetencia/', views.registrarCompetencia),
    path('editarCompetencia/<id>', views.editarCompetencia),
    path('edicionCompetencia/', views.edicionCompetencia),
    path('eliminarCompetencia/<id>', views.eliminarCompetencia),
    #Sesion
    path('login/', views.login)
]
