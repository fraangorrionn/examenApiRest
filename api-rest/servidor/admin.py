from django.contrib import admin
from .models import (
    Usuario, 
    MobileApp, 
    Comentario,
    ClienteAPP,
    CreadorDeAplicaciones, 
)

admin.site.register(Usuario)
admin.site.register(MobileApp)
admin.site.register(Comentario)
admin.site.register(ClienteAPP)
admin.site.register(CreadorDeAplicaciones)