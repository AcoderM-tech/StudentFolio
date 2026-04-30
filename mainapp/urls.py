from django.urls import path
from . import views

urlpatterns = [

    # ── Asosiy sahifa ─────────────────────────────────────
    path('',views.landing_view,name='home'),
    path('login/',views.login_view,name='login'),
    path('register/',views.register,name='register'),
    path('about/',views.about,name='about'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('dashboard/profil/',views.profil_form,name='profil_form'),
    path('dashboard/logout/',views.logout_view,name='logout'),
    path('dashboard/projects/',views.project_view,name='projects'),
    path('dashboard/certificates/',views.sertifikat_view,name='certificates'),
    path('dashboard/achievements/',views.yutuqlar_view,name='achievements'),
    path('dashboard/experiences/',views.ish_view,name='experiences'),
    path('dashboard/projects/add/', views.add_projects, name='add_project'),
    path('dashboard/certificates/add/', views.add_certificate, name='add_certificate'),
    path('dashboard/achievements/add/', views.add_achievement, name='add_achievement'),
    path('dashboard/experiences/add/', views.add_ish, name='add_experience'),
    path('dashboard/projects/edit/<int:pk>/', views.edit_project, name='edit_project'),
    path('dashboard/projects/delete/<int:pk>/', views.del_project, name='del_project'),
    path('dashboard/experiences/delete/<int:pk>/', views.del_job, name='delete_experience'),
    path('dashboard/experiences/edit/<int:pk>/', views.edit_job, name='edit_experience'),
    path('dashboard/achievements/edit/<int:pk>/', views.edit_achievement, name='edit_achievement'),
    path('dashboard/achievements/delete/<int:pk>/', views.delete_achievement, name='delete_achievement'),
    path('dashboard/certificates/edit/<int:pk>/', views.edit_certificate, name='edit_certificate'),
    path('dashboard/certificates/delete/<int:pk>/', views.delete_certificate, name='delete_certificate'),
    path('dashboard/cv-generator/', views.cv_generator_page, name='cv_generator'),
]

