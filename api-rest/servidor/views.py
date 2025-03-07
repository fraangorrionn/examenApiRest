from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import Group
from datetime import datetime
from django.contrib.auth.decorators import permission_required


def index(request):
    if 'fecha_inicio' not in request.session:
        request.session['fecha_inicio'] = str(datetime.now())

    return render(request, 'index.html', {'fecha_inicio': request.session['fecha_inicio']})

@permission_required('servidor.view_usuario')
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

@permission_required('servidor.view_mobileapp')
def lista_apps(request):
    apps = MobileApp.objects.all()
    return render(request, 'apps/lista_apps.html', {'apps': apps})

@permission_required('servidor.view_comentario')
def lista_comentarios(request):
    comentarios = Comentario.objects.all()
    return render(request, 'comentarios/lista_comentarios.html', {'comentarios': comentarios})


### CRUD PARA USUARIOS ###

# 🔹 Crear usuario
@permission_required('servidor.add_usuario')
def crear_usuario(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/crear_usuario.html', {'form': form})

### BÚSQUEDA AVANZADA DE USUARIOS ###
@permission_required('servidor.view_usuario')
def buscar_usuarios(request):
    form = UsuarioBusquedaForm(request.GET)
    usuarios = Usuario.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        rol = form.cleaned_data.get('rol')
        fecha_registro_desde = form.cleaned_data.get('fecha_registro_desde')
        fecha_registro_hasta = form.cleaned_data.get('fecha_registro_hasta')
        ultima_conexion_desde = form.cleaned_data.get('ultima_conexion_desde')
        ultima_conexion_hasta = form.cleaned_data.get('ultima_conexion_hasta')
        email_confirmado = form.cleaned_data.get('email_confirmado')
        biografia = form.cleaned_data.get('biografia')
        telefono = form.cleaned_data.get('telefono')

        filtros = Q()

        if query:
            filtros |= Q(username__icontains=query) | Q(email__icontains=query) | Q(biografia__icontains=query) | Q(telefono__icontains=query)

        if username:
            filtros &= Q(username__icontains=username)
        if email:
            filtros &= Q(email__icontains=email)
        if rol:
            filtros &= Q(rol=rol)
        if fecha_registro_desde:
            filtros &= Q(fecha_registro__gte=fecha_registro_desde)
        if fecha_registro_hasta:
            filtros &= Q(fecha_registro__lte=fecha_registro_hasta)
        if ultima_conexion_desde:
            filtros &= Q(ultima_conexion__gte=ultima_conexion_desde)
        if ultima_conexion_hasta:
            filtros &= Q(ultima_conexion__lte=ultima_conexion_hasta)
        if email_confirmado:
            filtros &= Q(email_confirmado=email_confirmado)
        if biografia:
            filtros &= Q(biografia__icontains=biografia)
        if telefono:
            filtros &= Q(telefono__icontains=telefono)

        usuarios = usuarios.filter(filtros)

    return render(request, 'usuarios/buscar_usuarios.html', {'usuarios': usuarios, 'form': form})


# 🔹 Editar usuario
@permission_required('servidor.change_usuario')
def editar_usuario(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuarios/editar_usuario.html', {'form': form})

# 🔹 Eliminar usuario
@permission_required('servidor.delete_usuario')
def eliminar_usuario(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    if request.method == "POST":
        usuario.delete()
        return redirect('lista_usuarios')
    return render(request, 'usuarios/eliminar_usuario.html', {'usuario': usuario})


### CREAR UNA APP ###
@permission_required('servidor.add_mobileapp')
def crear_app(request):
    if request.method == "POST":
        form = MobileAppForm(request.POST, usuario=request.user)
        if form.is_valid():
            form.save()  # Se asigna automáticamente el usuario autenticado
            messages.success(request, "Aplicación creada exitosamente.")
            return redirect('lista_apps')
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = MobileAppForm(usuario=request.user)

    return render(request, 'apps/crear_app.html', {'form': form})


### BÚSQUEDA AVANZADA ###
@permission_required('servidor.view_mobileapp')
def buscar_apps(request):
    form = MobileAppBusquedaForm(request.GET)
    apps = MobileApp.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        categoria = form.cleaned_data.get('categoria')
        desarrollador = form.cleaned_data.get('desarrollador')
        fecha_creacion_desde = form.cleaned_data.get('fecha_creacion_desde')
        fecha_creacion_hasta = form.cleaned_data.get('fecha_creacion_hasta')
        descargas_minimas = form.cleaned_data.get('descargas_minimas')
        descargas_maximas = form.cleaned_data.get('descargas_maximas')

        filtros = Q()

        if query:
            filtros |= Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        if categoria:
            filtros &= Q(categoria__icontains=categoria)
        if desarrollador:
            filtros &= Q(desarrollador__username__icontains=desarrollador)
        if fecha_creacion_desde:
            filtros &= Q(fecha_creacion__gte=fecha_creacion_desde)
        if fecha_creacion_hasta:
            filtros &= Q(fecha_creacion__lte=fecha_creacion_hasta)
        if descargas_minimas:
            filtros &= Q(descargas__gte=descargas_minimas)
        if descargas_maximas:
            filtros &= Q(descargas__lte=descargas_maximas)

        apps = apps.filter(filtros)

    return render(request, 'apps/buscar_app.html', {'apps': apps, 'form': form})


### EDITAR APP ###
@permission_required('servidor.change_mobileapp')
def editar_app(request, app_id):
    try:
        app = MobileApp.objects.get(id=app_id)
    except MobileApp.DoesNotExist:
        messages.error(request, "La aplicación no existe.")
        return redirect('lista_apps')

    form = MobileAppForm(instance=app)
    if request.method == "POST":
        form = MobileAppForm(request.POST, instance=app)
        if form.is_valid():
            form.save()
            messages.success(request, "Aplicación editada correctamente.")
            return redirect('lista_apps')
        else:
            messages.error(request, "Corrige los errores en el formulario.")

    return render(request, 'apps/editar_app.html', {'form': form})

### ELIMINAR APP ###
@permission_required('servidor.delete_mobileapp')
def eliminar_app(request, app_id):
    try:
        app = MobileApp.objects.get(id=app_id)
    except MobileApp.DoesNotExist:
        messages.error(request, "La aplicación no existe.")
        return redirect('lista_apps')

    if request.method == "POST":
        app.delete()
        messages.success(request, "Aplicación eliminada correctamente.")
        return redirect('lista_apps')

    return render(request, 'apps/eliminar_app.html', {'app': app})

### CREAR UN COMENTARIO ###
@permission_required('servidor.add_comentario')
def crear_comentario(request):
    if request.method == "POST":
        form = ComentarioForm(request.POST, usuario=request.user)  # Pasar request.user directamente
        if form.is_valid():
            form.save()
            messages.success(request, "Comentario agregado exitosamente.")
            return redirect('lista_comentarios')
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = ComentarioForm(usuario=request.user)

    return render(request, 'comentarios/crear_comentario.html', {'form': form})


### BÚSQUEDA AVANZADA ###
@permission_required('servidor.view_comentario')
def buscar_comentarios(request):
    form = ComentarioBusquedaForm(request.GET)
    comentarios = Comentario.objects.all()

    print("BÚSQUEDA EJECUTADA")  # Verificar que la vista se ejecuta

    if form.is_valid():
        query = form.cleaned_data.get('query')
        app = form.cleaned_data.get('app')
        usuario = form.cleaned_data.get('usuario')
        fecha_creacion_desde = form.cleaned_data.get('fecha_creacion_desde')
        fecha_creacion_hasta = form.cleaned_data.get('fecha_creacion_hasta')
        calificacion_minima = form.cleaned_data.get('calificacion_minima')
        calificacion_maxima = form.cleaned_data.get('calificacion_maxima')
        editado = form.cleaned_data.get('editado')

        filtros = Q()

        if query:
            filtros |= Q(texto__icontains=query) | Q(respuesta__icontains=query)
        if app:
            filtros &= Q(app__nombre__icontains=app)
        if usuario:
            filtros &= Q(usuario__username__icontains=usuario)
        if fecha_creacion_desde:
            filtros &= Q(fecha_creacion__gte=fecha_creacion_desde)
        if fecha_creacion_hasta:
            filtros &= Q(fecha_creacion__lte=fecha_creacion_hasta)
        if calificacion_minima:
            filtros &= Q(calificacion__gte=calificacion_minima)
        if calificacion_maxima:
            filtros &= Q(calificacion__lte=calificacion_maxima)
        if editado:
            filtros &= Q(editado=True)

        print("Filtros aplicados:", filtros)  # Ver los filtros que se están aplicando

        comentarios = comentarios.filter(filtros)

    print("Resultados encontrados:", comentarios.count())  # Ver cuántos comentarios devuelve la búsqueda

    return render(request, 'comentarios/buscar_comentario.html', {'comentarios': comentarios, 'form': form})

### EDITAR COMENTARIO ###
@permission_required('servidor.change_comentario')
def editar_comentario(request, comentario_id):
    try:
        comentario = Comentario.objects.get(id=comentario_id)
    except Comentario.DoesNotExist:
        messages.error(request, "El comentario no existe.")
        return redirect('lista_comentarios')

    form = ComentarioForm(instance=comentario)
    if request.method == "POST":
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            messages.success(request, "Comentario editado correctamente.")
            return redirect('lista_comentarios')
        else:
            messages.error(request, "Corrige los errores en el formulario.")

    return render(request, 'comentarios/editar_comentario.html', {'form': form})

### ELIMINAR COMENTARIO ###
@permission_required('servidor.delete_comentario')
def eliminar_comentario(request, comentario_id):
    try:
        comentario = Comentario.objects.get(id=comentario_id)
    except Comentario.DoesNotExist:
        messages.error(request, "El comentario no existe.")
        return redirect('lista_comentarios')

    if request.method == "POST":
        comentario.delete()
        messages.success(request, "Comentario eliminado correctamente.")
        return redirect('lista_comentarios')

    return render(request, 'comentarios/eliminar_comentario.html', {'comentario': comentario})


def registrar_usuario(request):
    if request.method == 'POST':
        formulario = RegistroUsuarioForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()
            rol = int(formulario.cleaned_data.get('rol'))

            if rol == Usuario.CLIENTE:
                grupo, _ = Group.objects.get_or_create(name='ClientesApp')  # Asegurar que el grupo existe
                grupo.user_set.add(user)
                ClienteAPP.objects.create(usuario=user)  # Se crea automáticamente

            elif rol == Usuario.CREATOR:
                grupo, _ = Group.objects.get_or_create(name='CreadorDeAplicaciones') 
                grupo.user_set.add(user)
                CreadorDeAplicaciones.objects.create(usuario=user)  

            login(request, user)
            return redirect('index')
    else:
        formulario = RegistroUsuarioForm()

    return render(request, 'registration/signup.html', {'formulario': formulario})

