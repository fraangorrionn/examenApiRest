from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class Usuario(AbstractUser):
    ADMINISTRADOR = 1
    CREATOR = 2
    CLIENTE = 3
    ROLES = (
        (ADMINISTRADOR, 'Administrador'),
        (CREATOR, 'CreadorDeAplicaciones'),
        (CLIENTE, 'ClienteAPP'),
    )

    rol = models.PositiveSmallIntegerField(choices=ROLES, default=CLIENTE)
    email_confirmado = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultima_conexion = models.DateTimeField(auto_now=True)
    biografia = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

class CreadorDeAplicaciones(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    apps_creadas = models.ManyToManyField('MobileApp', blank=True, related_name='creadores')

    def __str__(self):
        return f"Creador: {self.usuario.username}"

class ClienteAPP(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    apps_favoritas = models.ManyToManyField('MobileApp', blank=True, related_name='usuarios_favoritos')

    def __str__(self):
        return f"Cliente: {self.usuario.username}"


class MobileApp(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now,blank=True)
    
    def __str__(self):
        return self.nombre


class Comentario(models.Model):
    texto = models.TextField()
    app = models.ForeignKey(MobileApp, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comentarios')
    fecha_creacion = models.DateTimeField(default=timezone.now,blank=True)
    calificacion = models.PositiveSmallIntegerField(default=5)


    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.app.nombre}"

