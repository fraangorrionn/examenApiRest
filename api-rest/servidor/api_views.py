from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .forms import *


# VISTA GET PARA OBTENER TODOS LOS USUARIOS
@api_view(['GET'])
def obtener_usuarios(request):
    usuarios = Usuario.objects.all()
    serializer = UsuarioSerializer(usuarios, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# VISTA GET PARA OBTENER TODAS LAS APPS
@api_view(['GET'])
def obtener_apps(request):
    apps = MobileApp.objects.all()
    serializer = MobileAppSerializer(apps, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# VISTA GET PARA OBTENER TODOS LOS COMENTARIOS
@api_view(['GET'])
def obtener_comentarios(request):
    comentarios = Comentario.objects.all()
    serializer = ComentarioSerializer(comentarios, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def buscar_usuarios(request):
    """
    Vista para la búsqueda avanzada de usuarios.
    """
    # Si hay parámetros en la query
    if len(request.query_params) > 0:
        formulario = UsuarioBusquedaForm(request.query_params)

        if formulario.is_valid():
            # Obtener los datos del formulario ya validados
            query = formulario.cleaned_data.get("query")
            username = formulario.cleaned_data.get("username")
            email = formulario.cleaned_data.get("email")
            rol = formulario.cleaned_data.get("rol")
            fecha_registro_desde = formulario.cleaned_data.get("fecha_registro_desde")
            fecha_registro_hasta = formulario.cleaned_data.get("fecha_registro_hasta")

            # Si todos los campos están vacíos, devolver un error
            if not any([query, username, email, rol, fecha_registro_desde, fecha_registro_hasta]):
                return Response({"error": "Debe proporcionar al menos un parámetro de búsqueda."}, status=status.HTTP_400_BAD_REQUEST)

            # Construir el QuerySet inicial
            usuarios = Usuario.objects.all()

            # Aplicar filtros
            if query:
                usuarios = usuarios.filter(username__icontains=query) | usuarios.filter(email__icontains=query)

            if username:
                usuarios = usuarios.filter(username__icontains=username)

            if email:
                usuarios = usuarios.filter(email__icontains=email)

            if rol:
                usuarios = usuarios.filter(rol=rol)

            if fecha_registro_desde:
                usuarios = usuarios.filter(fecha_registro__gte=fecha_registro_desde)

            if fecha_registro_hasta:
                usuarios = usuarios.filter(fecha_registro__lte=fecha_registro_hasta)

            # Serializar los resultados
            serializer = UsuarioSerializer(usuarios, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            # Si el formulario no es válido, devolver errores
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        # Si no hay parámetros en la query
        return Response({"error": "Debe proporcionar al menos un parámetro de búsqueda."}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def buscar_apps(request):
    # Si hay parámetros en la query
    if len(request.query_params) > 0:
        formulario = MobileAppBusquedaForm(request.query_params)

        if formulario.is_valid():
            # Obtener los datos del formulario
            query = formulario.cleaned_data.get('query')
            categoria = formulario.cleaned_data.get('categoria')
            desarrollador = formulario.cleaned_data.get('desarrollador')
            fecha_creacion_desde = formulario.cleaned_data.get('fecha_creacion_desde')
            fecha_creacion_hasta = formulario.cleaned_data.get('fecha_creacion_hasta')
            descargas_minimas = formulario.cleaned_data.get('descargas_minimas')
            descargas_maximas = formulario.cleaned_data.get('descargas_maximas')

            # Si todos los campos están vacíos, devolver un error
            if not any([query, categoria, desarrollador, fecha_creacion_desde, fecha_creacion_hasta, descargas_minimas, descargas_maximas]):
                return Response({"error": "Debe proporcionar al menos un parámetro de búsqueda."}, status=status.HTTP_400_BAD_REQUEST)

            # Construir la QuerySet inicial
            QSapps = MobileApp.objects.all()

            # Filtros por nombre o descripción
            if query:
                QSapps = QSapps.filter(models.Q(nombre__icontains=query) | models.Q(descripcion__icontains=query))

            # Filtro por categoría
            if categoria:
                QSapps = QSapps.filter(categoria__icontains=categoria)

            # Filtro por desarrollador
            if desarrollador:
                QSapps = QSapps.filter(desarrollador__usuario__username__icontains=desarrollador)

            # Filtro por fecha de creación
            if fecha_creacion_desde:
                QSapps = QSapps.filter(fecha_creacion__date__gte=fecha_creacion_desde)

            if fecha_creacion_hasta:
                QSapps = QSapps.filter(fecha_creacion__date__lte=fecha_creacion_hasta)

            # Filtro por número de descargas
            if descargas_minimas:
                QSapps = QSapps.filter(descargas__gte=descargas_minimas)

            if descargas_maximas:
                QSapps = QSapps.filter(descargas__lte=descargas_maximas)

            # Serializar los resultados
            serializer = MobileAppSerializer(QSapps, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            # Si el formulario no es válido, devolvemos los errores del formulario
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        # Si no hay parámetros en la query
        return Response({"error": "Debe proporcionar al menos un parámetro de búsqueda."}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def buscar_comentarios(request):
    if len(request.query_params) > 0:  # Si hay parámetros en la consulta
        formulario = ComentarioBusquedaForm(request.query_params)
        
        if formulario.is_valid():
            # Obtener valores del formulario limpio
            query = formulario.cleaned_data.get('query')
            app = formulario.cleaned_data.get('app')
            usuario = formulario.cleaned_data.get('usuario')
            fecha_creacion_desde = formulario.cleaned_data.get('fecha_creacion_desde')
            fecha_creacion_hasta = formulario.cleaned_data.get('fecha_creacion_hasta')
            calificacion_minima = formulario.cleaned_data.get('calificacion_minima')
            calificacion_maxima = formulario.cleaned_data.get('calificacion_maxima')

            # Construcción de la consulta
            comentarios = Comentario.objects.all()

            if query:
                comentarios = comentarios.filter(texto__icontains=query)

            if app:
                comentarios = comentarios.filter(app__nombre__icontains=app)

            if usuario:
                comentarios = comentarios.filter(usuario__username__icontains=usuario)

            if fecha_creacion_desde:
                comentarios = comentarios.filter(fecha_creacion__date__gte=fecha_creacion_desde)

            if fecha_creacion_hasta:
                comentarios = comentarios.filter(fecha_creacion__date__lte=fecha_creacion_hasta)

            if calificacion_minima:
                comentarios = comentarios.filter(calificacion__gte=calificacion_minima)

            if calificacion_maxima:
                comentarios = comentarios.filter(calificacion__lte=calificacion_maxima)

            # Serialización de resultados
            serializer = ComentarioSerializer(comentarios, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"error": "Debes proporcionar al menos un parámetro de búsqueda."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def crear_usuario(request):
    serializer = UsuarioSerializerCreate(data=request.data)
    
    if serializer.is_valid():
        try:
            serializer.save()
            return Response({"mensaje": "Usuario creado exitosamente"}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def crear_comentario(request):
    print(request.data)  # Debug: Ver datos recibidos
    comentario_serializer = ComentarioCreateSerializer(data=request.data)

    if comentario_serializer.is_valid():
        try:
            comentario_serializer.save()
            return Response({"mensaje": "Comentario creado exitosamente"}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(repr(error))  # Debug en la consola
            return Response({"error": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(comentario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT'])
def comentario_editar(request, comentario_id):
    print(f"Solicitud recibida en comentario_editar con ID: {comentario_id}, Método: {request.method}")

    try:
        comentario = Comentario.objects.get(id=comentario_id)
    except Comentario.DoesNotExist:
        return Response({"error": "Comentario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        comentario_serializer = ComentarioCreateSerializer(comentario)
        return Response(comentario_serializer.data)

    comentario_serializer = ComentarioCreateSerializer(instance=comentario, data=request.data)

    if comentario_serializer.is_valid():
        try:
            comentario_serializer.save()
            return Response({"mensaje": "Comentario editado correctamente"}, status=status.HTTP_200_OK)
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({"error": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(comentario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def comentario_actualizar_texto(request, comentario_id):
    try:
        comentario = Comentario.objects.get(id=comentario_id)
    except Comentario.DoesNotExist:
        return Response({"detail": "Comentario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ComentarioActualizarSerializer(data=request.data, instance=comentario, partial=True)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Comentario actualizado con éxito", status=status.HTTP_200_OK)
        except Exception as error:
            print(repr(error)) 
            return Response({"detail": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def comentario_eliminar(request, comentario_id):
    try:
        comentario = Comentario.objects.get(id=comentario_id)
    except Comentario.DoesNotExist:
        return Response({"detail": "Comentario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    try:
        comentario.delete()
        return Response("Comentario ELIMINADO", status=status.HTTP_200_OK)
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)