from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from salusApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name='home'),
    path('admin/', admin.site.urls),
    path('iniciar-sesion/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('salir-cuenta/', auth_views.LogoutView.as_view(), name='logout'),
    path('registrarse/', views.register, name='signup'),
    path('cambiar-clave/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html', success_url='changepass-success'), name='changepass'),
    path('cambiar-clave/logrado', views.change_password_success, name='changepass-success'),
    path('menu-principal/', views.show_dashboard, name='dashboard'),
    path('menu-principal/mi-clinica', views.show_clinic, name='mi-clinica'),
    path('menu-principal/mi-clinica/room/<int:room_id>', views.show_clinic_room, name='mi-clinica-room'),
    path('menu-principal/mi-clinica/room/create', views.create_room, name='room-add'),
    path('menu-principal/mi-clinica/room/<int:room_id>/delete', views.delete_room, name='room-delete'),
    path('menu-principal/mi-clinica/room/<int:room_id>/edit', views.edit_room, name='room-edit'),
    path('menu-principal/equipo', views.show_team, name='equipo'),
    path('menu-principal/equipo/enfermeros', views.show_nurses_list, name='enfermeros'),
    path('menu-principal/equipo/enfermeros/nuevo', views.create_nurses, name='enfermeros-add'),
    path('menu-principal/equipo/enfermeros/eliminar/<int:pk>', views.delete_nurses, name='enfermeros-delete'),
    path('menu-principal/equipo/enfermeros/editar/<int:pk>', views.update_nurses, name='enfermeros-edit'),
    path('menu-principal/equipo/doctores', views.show_doctors_list, name='doctores'),
    path('menu-principal/equipo/doctores/nuevo', views.create_doctor, name='doctores-add'),
    path('menu-principal/equipo/doctores/eliminar/<int:pk>', views.delete_doctor, name='doctores-delete'),
    path('menu-principal/equipo/doctores/editar/<int:pk>', views.update_doctor, name='doctores-edit'),
    path('menu-principal/equipo/pacientes', views.show_patient_list, name='pacientes'),
    path('menu-principal/equipo/pacientes/nuevo', views.create_patient, name='pacientes-add'),
    path('menu-principal/equipo/pacientes/editar/<int:pk>', views.update_patient, name='pacientes-edit'),
    path('menu-principal/equipo/pacientes/eliminar/<int:pk>', views.delete_patient, name='pacientes-delete'),
    path('menu-principal/configuracion', views.show_settings, name='settings'),
    path('menu-principal/configuracion/eliminar/<int:pk>', views.delete_user, name='delete'),
    path('menu-principal/configuracion/eliminar/<int:pk>#', views.confirm_delete, name='confirm-delete'),
]