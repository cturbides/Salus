from django.urls import path, include, reverse_lazy
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.register_view.as_view(), name='signup'),
    path('changepass/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html', success_url='changepass-success'), name='changepass'),
    path('changepass/changepass-success', views.change_password_success, name='changepass-success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/mi-clinica', views.dashboard_clinica, name='mi-clinica'),
    path('dashboard/analitica', views.dashboard_clinica, name='analitica'),
    path('dashboard/equipo', views.dashboard_equipo, name='equipo'),
    path('dashboard/equipo/doctores', views.dashboard_equipo_doctores, name='doctores'),
    path('dashboard/equipo/enfermeros', views.dashboard_equipo_enfermeros, name='enfermeros'),
    path('dashboard/equipo/pacientes', views.dashboard_equipo_pacientes, name='pacientes'),
    path('dashboard/settings', views.dashboard_clinica, name='settings'),
]

