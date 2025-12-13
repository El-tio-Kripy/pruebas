from django.db import models
import hashlib


class Usuarios(models.Model):
    # Constantes para los perfiles (coinciden con la pauta)
    PERFIL_ADMIN = 1
    PERFIL_TRABAJADOR = 2
    PERFIL_JEFE = 3

    PERFIL_CHOICES = (
        (PERFIL_ADMIN, "Administrador"),
        (PERFIL_TRABAJADOR, "Trabajador"),
        (PERFIL_JEFE, "Jefe de Sección"),
    )

    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    perfil = models.IntegerField(choices=PERFIL_CHOICES)
    nombre = models.CharField(max_length=200)
    email = models.EmailField()
    # Hash solo lectura en admin
    hash = models.CharField(max_length=128, editable=False)

    def save(self, *args, **kwargs):
        """
        Genera el hash SHA256 a partir del password en texto plano.
        Esto se ejecuta cada vez que se guarda el usuario.
        """
        if self.password:
            self.hash = hashlib.sha256(
                self.password.encode("utf-8")
            ).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.get_perfil_display()})"
