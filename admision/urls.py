from django.urls import path
from . import views  # Importa las vistas de la aplicación



urlpatterns = [
    path('', views.home, name='home'),  # Página de inicio
    path('pacientes/', views.listado_pacientes, name='listado_pacientes'),  # Listado de pacientes
    path('pacientes/detalle/<int:id>/', views.detalle_paciente, name='detalle_paciente'),  # Detalle de paciente
    path('pacientes/agregar/', views.agregar_paciente, name='agregar_paciente'),  # Agregar paciente
    path('pacientes/editar/<int:id>/', views.editar_paciente, name='editar_paciente'),  # Editar paciente
    path('pacientes/buscar/', views.buscar_paciente, name='buscar_paciente'),  # Buscar paciente


]