from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'rol', 'email_confirmado', 'biografia', 'telefono']

class UsuarioBusquedaForm(forms.Form):
    query = forms.CharField(
        required=False,
        label="Búsqueda Global",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar en todos los campos'})
    )
    username = forms.CharField(
        required=False, 
        label="Nombre de Usuario",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=False, 
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    rol = forms.ChoiceField(
        required=False, 
        label="Rol", 
        choices=[('', 'Todos')] + list(Usuario.ROLES),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    fecha_registro_desde = forms.DateField(
        required=False,
        label="Registrado Desde",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    fecha_registro_hasta = forms.DateField(
        required=False,
        label="Registrado Hasta",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    ultima_conexion_desde = forms.DateField(
        required=False,
        label="Última Conexión Desde",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    ultima_conexion_hasta = forms.DateField(
        required=False,
        label="Última Conexión Hasta",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    email_confirmado = forms.BooleanField(
        required=False,
        label="Email Confirmado",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    biografia = forms.CharField(
        required=False,
        label="Biografía",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    telefono = forms.CharField(
        required=False,
        label="Teléfono",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        query = cleaned_data.get('query')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        rol = cleaned_data.get('rol')
        fecha_registro_desde = cleaned_data.get('fecha_registro_desde')
        fecha_registro_hasta = cleaned_data.get('fecha_registro_hasta')
        ultima_conexion_desde = cleaned_data.get('ultima_conexion_desde')
        ultima_conexion_hasta = cleaned_data.get('ultima_conexion_hasta')
        biografia = cleaned_data.get('biografia')
        telefono = cleaned_data.get('telefono')

        if not any([query, username, email, rol, fecha_registro_desde, fecha_registro_hasta, ultima_conexion_desde, ultima_conexion_hasta, biografia, telefono]):
            self.add_error(None, "Debes ingresar al menos un criterio de búsqueda.")

        if fecha_registro_desde and fecha_registro_hasta and fecha_registro_desde > fecha_registro_hasta:
            self.add_error('fecha_registro_hasta', "La fecha de registro hasta no puede ser menor que la fecha de registro desde.")

        if ultima_conexion_desde and ultima_conexion_hasta and ultima_conexion_desde > ultima_conexion_hasta:
            self.add_error('ultima_conexion_hasta', "La fecha de última conexión hasta no puede ser menor que la fecha de última conexión desde.")

        return cleaned_data

class MobileAppForm(forms.ModelForm):
    class Meta:
        model = MobileApp
        fields = ['nombre', 'descripcion', 'categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        app = super().save(commit=False)
        if self.usuario:
            creador = CreadorDeAplicaciones.objects.filter(usuario=self.usuario).first()
            if not creador:
                self.add_error(None, "Solo los Creadores de Aplicaciones pueden registrar una app.")
                return None  # No se guarda
            app.desarrollador = creador
        if commit:
            app.save()
        return app




class MobileAppBusquedaForm(forms.Form):
    query = forms.CharField(
        required=False,
        label="Buscar Aplicación",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre o Descripción'})
    )
    categoria = forms.CharField(
        required=False,
        label="Categoría",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    desarrollador = forms.CharField(
        required=False,
        label="Desarrollador",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    fecha_creacion_desde = forms.DateField(
        required=False,
        label="Creada Desde",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    fecha_creacion_hasta = forms.DateField(
        required=False,
        label="Creada Hasta",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    descargas_minimas = forms.IntegerField(
        required=False,
        label="Mínimo de Descargas",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0})
    )
    descargas_maximas = forms.IntegerField(
        required=False,
        label="Máximo de Descargas",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0})
    )

    def clean(self):
        cleaned_data = super().clean()
        query = cleaned_data.get('query')
        categoria = cleaned_data.get('categoria')
        desarrollador = cleaned_data.get('desarrollador')
        fecha_creacion_desde = cleaned_data.get('fecha_creacion_desde')
        fecha_creacion_hasta = cleaned_data.get('fecha_creacion_hasta')
        descargas_minimas = cleaned_data.get('descargas_minimas')
        descargas_maximas = cleaned_data.get('descargas_maximas')

        if not any([query, categoria, desarrollador, fecha_creacion_desde, fecha_creacion_hasta, descargas_minimas, descargas_maximas]):
            self.add_error(None, "Debes ingresar al menos un criterio de búsqueda.")

        if fecha_creacion_desde and fecha_creacion_hasta and fecha_creacion_desde > fecha_creacion_hasta:
            self.add_error('fecha_creacion_hasta', "La fecha de creación hasta no puede ser menor que la fecha desde.")

        if descargas_minimas and descargas_maximas and descargas_minimas > descargas_maximas:
            self.add_error('descargas_maximas', "El número máximo de descargas no puede ser menor que el mínimo.")

        return cleaned_data


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto', 'calificacion', 'app']
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe tu comentario...'}),
            'calificacion': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'app': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comentario = super().save(commit=False)
        if self.usuario:
            comentario.usuario = self.usuario  # Asignar usuario autenticado sin validación extra
        if commit:
            comentario.save()
        return comentario




class ComentarioBusquedaForm(forms.Form):
    query = forms.CharField(
        required=False,
        label="Buscar Comentario",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Texto o Respuesta'})
    )
    app = forms.CharField(
        required=False,
        label="Aplicación",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    usuario = forms.CharField(
        required=False,
        label="Usuario",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    fecha_creacion_desde = forms.DateField(
        required=False,
        label="Fecha Desde",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    fecha_creacion_hasta = forms.DateField(
        required=False,
        label="Fecha Hasta",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    calificacion_minima = forms.IntegerField(
        required=False,
        label="Calificación Mínima",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5})
    )
    calificacion_maxima = forms.IntegerField(
        required=False,
        label="Calificación Máxima",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5})
    )
    editado = forms.BooleanField(
        required=False,
        label="Editado",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def clean(self):
        cleaned_data = super().clean()
        query = cleaned_data.get('query')
        app = cleaned_data.get('app')
        usuario = cleaned_data.get('usuario')
        fecha_creacion_desde = cleaned_data.get('fecha_creacion_desde')
        fecha_creacion_hasta = cleaned_data.get('fecha_creacion_hasta')
        calificacion_minima = cleaned_data.get('calificacion_minima')
        calificacion_maxima = cleaned_data.get('calificacion_maxima')

        if not any([query, app, usuario, fecha_creacion_desde, fecha_creacion_hasta, calificacion_minima, calificacion_maxima]):
            self.add_error(None, "Debes ingresar al menos un criterio de búsqueda.")

        if fecha_creacion_desde and fecha_creacion_hasta and fecha_creacion_desde > fecha_creacion_hasta:
            self.add_error('fecha_creacion_hasta', "La fecha hasta no puede ser menor que la fecha desde.")

        if calificacion_minima and calificacion_maxima and calificacion_minima > calificacion_maxima:
            self.add_error('calificacion_maxima', "La calificación máxima no puede ser menor que la mínima.")

        return cleaned_data


class RegistroUsuarioForm(UserCreationForm):
    roles = (
        (Usuario.CLIENTE, 'ClienteAPP'),
        (Usuario.CREATOR, 'CreadorDeAplicaciones'),
    )

    rol = forms.ChoiceField(choices=roles, label="Rol del usuario", widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2', 'rol')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

