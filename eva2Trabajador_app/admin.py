from django.contrib import admin
from django import forms

from .models import Trabajador, Afps, Descuentos, Liquidaciones
from .forms import DescuentosForm, LiquidacionesForm


# --------------------------------------------------------------------
# Formulario para Trabajador: convierte afp (CharField) en un SELECT
# basado en la tabla Afps, pero sigue guardando el nombre como texto.
# --------------------------------------------------------------------
class TrabajadorAdminForm(forms.ModelForm):
    afp = forms.ModelChoiceField(
        queryset=Afps.objects.all(),
        to_field_name="nombre",
        label="AFP",
        required=True,
    )

    class Meta:
        model = Trabajador
        fields = "__all__"

    def clean_afp(self):
        # Guardamos finalmente el nombre de la AFP (string),
        # porque en el modelo Trabajador.afp es un CharField.
        afp_obj = self.cleaned_data["afp"]
        return afp_obj.nombre


# --------------------------------------------------------------------
# Admin Afps
# --------------------------------------------------------------------
@admin.register(Afps)
class AfpsAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "descuento")
    search_fields = ("nombre",)


# --------------------------------------------------------------------
# Admin Trabajador (usa formulario personalizado)
# --------------------------------------------------------------------
@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    form = TrabajadorAdminForm
    list_display = ("rut", "nombre", "base", "afp")
    search_fields = ("rut", "nombre")
    list_filter = ("afp",)
    # OJO: no ponemos "afp" en list_editable porque usamos un ModelForm
    # personalizado, y eso suele dar conflictos en el admin.


# --------------------------------------------------------------------
# Admin Descuentos (usa DescuentosForm)
# --------------------------------------------------------------------
@admin.register(Descuentos)
class DescuentosAdmin(admin.ModelAdmin):
    form = DescuentosForm
    list_display = ("rut", "fecha", "concepto", "monto")
    search_fields = ("rut", "concepto")
    list_filter = ("fecha",)


# --------------------------------------------------------------------
# Admin Liquidaciones (usa LiquidacionesForm)
# --------------------------------------------------------------------
@admin.register(Liquidaciones)
class LiquidacionesAdmin(admin.ModelAdmin):
    form = LiquidacionesForm
    list_display = (
        "rut",
        "mes",
        "anio",
        "sbase",
        "sbruto",
        "desc_afp",
        "descuentos",
        "descuentos_totales",
        "sueldo_liquido",
    )
    search_fields = ("rut",)
    list_filter = ("anio", "mes")

    # Opcional pero muy recomendable:
    # estos campos se calculan, no se deberían editar a mano.
    readonly_fields = (
        "sbase",
        "sbruto",
        "desc_afp",
        "descuentos",
        "descuentos_totales",
        "sueldo_liquido",
    )
