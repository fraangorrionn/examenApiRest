from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
      
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/buscar/', views.buscar_usuarios, name='buscar_usuarios'),
    path('usuarios/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    
    path('apps/', views.lista_apps, name='lista_apps'),
    path('apps/crear/', views.crear_app, name='crear_app'),
    path('apps/buscar/', views.buscar_apps, name='buscar_apps'),
    path('apps/editar/<int:app_id>/', views.editar_app, name='editar_app'),
    path('apps/eliminar/<int:app_id>/', views.eliminar_app, name='eliminar_app'),
    
    path('comentarios/', views.lista_comentarios, name='lista_comentarios'),
    path('comentarios/crear/', views.crear_comentario, name='crear_comentario'),
    path('comentarios/buscar/', views.buscar_comentarios, name='buscar_comentarios'),
    path('comentarios/editar/<int:comentario_id>/', views.editar_comentario, name='editar_comentario'),
    path('comentarios/eliminar/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),
]

