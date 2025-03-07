from django.urls import path
from .api_views import *

urlpatterns = [
    # obtener datos con GET
    path('usuarios/', obtener_usuarios, name='api_usuarios'),
    path('apps/', obtener_apps, name='api_apps'),
    path('comentarios/', obtener_comentarios, name='api_comentarios'),
    
    #Usuarios
    path('usuarios/crear/', crear_usuario, name='crear_usuario'), 
    path('usuarios/buscar/', buscar_usuarios, name='buscar_usuarios'),
    
    #Apps
    path('apps/buscar/', buscar_apps, name='buscar_apps'),
    
    #Comentarios
    path('comentarios/crear/', crear_comentario, name='crear_comentario'),
    path('comentarios/buscar/', buscar_comentarios, name='buscar_comentarios'),
    path('comentarios/editar/<int:comentario_id>/', comentario_editar, name='comentario_editar'),
    path('comentarios/actualizar-texto/<int:comentario_id>/', comentario_actualizar_texto, name='comentario_actualizar_texto'),
    path('comentarios/eliminar/<int:comentario_id>/', comentario_eliminar, name='comentario_eliminar'),
    
    
    path('registration/registro', registrar_usuario, name='registrar_usuario'),

]