from rest_framework import serializers
from .models import *

# SERIALIZADOR DE USUARIO
class UsuarioSerializer(serializers.ModelSerializer):
    rol_display = serializers.CharField(source='get_rol_display', read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'email', 'rol', 'rol_display', 'email_confirmado',
            'fecha_registro', 'ultima_conexion', 'biografia', 'telefono'
        ]
        extra_kwargs = {
            'fecha_registro': {'format': '%d-%m-%Y'},
            'ultima_conexion': {'format': '%d-%m-%Y'}
        }

# SERIALIZADOR PARA EL CREADOR DE APLICACIONES
class CreadorDeAplicacionesSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)  # Muestra todos los datos del usuario

    class Meta:
        model = CreadorDeAplicaciones
        fields = ['usuario']

# SERIALIZADOR PARA EL CLIENTE
class ClienteAPPSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)  # Muestra todos los datos del usuario

    class Meta:
        model = ClienteAPP
        fields = ['usuario']

from datetime import datetime

class MobileAppSerializer(serializers.ModelSerializer):
    desarrollador = CreadorDeAplicacionesSerializer(read_only=True)  
    fecha_creacion = serializers.SerializerMethodField()  # Usamos SerializerMethodField para formatear manualmente

    class Meta:
        model = MobileApp
        fields = ['id', 'nombre', 'descripcion', 'fecha_creacion', 'desarrollador']

    def get_fecha_creacion(self, obj):
        return obj.fecha_creacion.strftime("%d-%m-%Y") if obj.fecha_creacion else None  # Convertimos manualmente la fecha


class ComentarioSerializer(serializers.ModelSerializer):
    usuario = serializers.SerializerMethodField()  
    app = serializers.StringRelatedField()  
    fecha_creacion = serializers.SerializerMethodField()  # Usamos SerializerMethodField

    class Meta:
        model = Comentario
        fields = ['id', 'texto', 'app', 'usuario', 'fecha_creacion', 'calificacion']

    def get_fecha_creacion(self, obj):
        return obj.fecha_creacion.strftime("%d-%m-%Y") if obj.fecha_creacion else None  # Convertimos manualmente

    def get_usuario(self, obj):
        if hasattr(obj.usuario, 'usuario'):
            return UsuarioSerializer(obj.usuario.usuario).data  
        return None

class UsuarioSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'rol', 'email_confirmado', 'biografia', 'telefono', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # La contraseña solo se escribe, no se lee

    def validate_email(self, email):
        """
        Validar que el email no esté ya registrado.
        """
        if Usuario.objects.filter(email=email).exists():
            raise serializers.ValidationError("Este email ya está registrado.")
        return email

    def validate_username(self, username):
        """
        Validar que el nombre de usuario sea único.
        """
        if Usuario.objects.filter(username=username).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def create(self, validated_data):
        """
        Crear un usuario con los datos validados y encriptar la contraseña.
        """
        password = validated_data.pop('password')  # Extraer la contraseña
        usuario = Usuario(**validated_data)  # Crear el usuario sin guardar aún
        usuario.set_password(password)  # Encriptar la contraseña
        usuario.save()  # Guardar usuario en la BD
        return usuario

class ComentarioCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ['texto', 'app', 'usuario', 'calificacion', 'respuesta']

    def validate_calificacion(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("La calificación debe estar entre 1 y 5.")
        return value

    def create(self, validated_data):
        return Comentario.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.texto = validated_data.get('texto', instance.texto)
        instance.calificacion = validated_data.get('calificacion', instance.calificacion)
        instance.respuesta = validated_data.get('respuesta', instance.respuesta)
        instance.save()
        return instance
    
class ComentarioActualizarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ['texto']  # Incluye solo el/los campo(s) que quieras actualizar

    def validate_texto(self, value):
        if not value.strip():
            raise serializers.ValidationError("El texto no puede estar vacío.")
        return value
