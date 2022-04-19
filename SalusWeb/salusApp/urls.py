from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name='home'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.register, name='signup'),
    path('changepass/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html', success_url='changepass-success'), name='changepass'),
    path('changepass/changepass-success', views.change_password_success, name='changepass-success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/mi-clinica', views.dashboard_clinica, name='mi-clinica'),
    path('dashboard/mi-clinica/<int:pk>', views.dashboard_clinica_room, name='mi-clinica-room'),
    path('dashboard/analitica', views.dashboard_clinica, name='analitica'),
    path('dashboard/equipo', views.dashboard_equipo, name='equipo'),
    path('dashboard/equipo/enfermeros', views.Enfermeros, name='enfermeros'),
    path('dashboard/equipo/enfermeros/add', views.EnfermerosCreate, name='enfermeros-add'),
    path('dashboard/equipo/enfermeros/delete/<int:pk>', views.EnfermerosDelete, name='enfermeros-delete'),
    path('dashboard/equipo/enfermeros/edit/<int:pk>', views.EnfermerosUpdate, name='enfermeros-edit'),
    path('dashboard/equipo/doctores', views.Doctores, name='doctores'),
    path('dashboard/equipo/doctores/add', views.DoctoresCreate, name='doctores-add'),
    path('dashboard/equipo/doctores/delete/<int:pk>', views.DoctoresDelete, name='doctores-delete'),
    path('dashboard/equipo/doctores/edit/<int:pk>', views.DoctoresUpdate, name='doctores-edit'),
    path('dashboard/equipo/pacientes', views.Pacientes, name='pacientes'),
    path('dashboard/equipo/pacientes/add', views.PacientesCreate, name='pacientes-add'),
    path('dashboard/equipo/pacientes/edit/<int:pk>', views.PacientesUpdate, name='pacientes-edit'),
    path('dashboard/equipo/pacientes/delete/<int:pk>', views.PacientesDelete, name='pacientes-delete'),
    path('dashboard/settings', views.dashboard_configuracion, name='settings'),
    path('dashboard/settings/delete/<int:pk>', views.delete_user, name='delete'),
    path('dashboard/settings/delete/<int:pk>#', views.confirm_delete, name='confirm-delete'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)