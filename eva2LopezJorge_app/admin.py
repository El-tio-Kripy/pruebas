from django.contrib import admin
from .models import Usuarios

@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    # Requisito EVA2: visualizar id, username, password, perfil, nombre, email y hash
    list_display = ("id", "username", "password", "perfil", "nombre", "email", "hash")

    # Requisito EVA2: username, password, perfil, nombre y email editables en línea
    # Nota Django: el primer campo de list_display no puede estar en list_editable (por eso 'id' queda fuera).
    list_editable = ("username", "password", "perfil", "nombre", "email")

    # Requisito EVA2: hash de solo lectura (se calcula automáticamente en el modelo)
    readonly_fields = ("hash",)

    # Requisito EVA2: búsqueda por nombre y correo
    search_fields = ("nombre", "email")

    # Requisito EVA2: filtrado por perfil
    list_filter = ("perfil",)
