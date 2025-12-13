from decimal import Decimal

from django import forms
from django.db.models import Sum

from .models import Trabajador, Descuentos, Liquidaciones, Afps


class DescuentosForm(forms.ModelForm):
    """
    Formulario de admin para Descuentos.

    Muestra un select de Trabajador y guarda automáticamente el rut
    del trabajador elegido en el campo rut del modelo.
    """

    trabajador = forms.ModelChoiceField(
        queryset=Trabajador.objects.all(),
        label="Trabajador",
        help_text="Selecciona el trabajador; el RUT se completará automáticamente.",
    )

    class Meta:
        model = Descuentos
        # No mostramos 'rut' en el formulario, solo el trabajador
        fields = ["trabajador", "fecha", "concepto", "monto"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si estamos editando un descuento existente, pre-seleccionamos al trabajador
        if self.instance and self.instance.pk:
            trabajador = Trabajador.objects.filter(rut=self.instance.rut).first()
            if trabajador:
                self.fields["trabajador"].initial = trabajador

    def save(self, commit=True):
        # Copiamos el rut del trabajador seleccionado al modelo
        trabajador = self.cleaned_data["trabajador"]
        self.instance.rut = trabajador.rut
        return super().save(commit)


class LiquidacionesForm(forms.ModelForm):
    """
    Formulario de admin para Liquidaciones.

    - El usuario elige un Trabajador (combo).
    - Se copia su RUT al campo rut.
    - Se calculan automáticamente:
        sbase, sbruto, desc_afp, descuentos, descuentos_totales, sueldo_liquido
      según la pauta del profesor.
    """

    trabajador = forms.ModelChoiceField(
        queryset=Trabajador.objects.all(),
        label="Trabajador",
        help_text="Selecciona el trabajador; el RUT se completará automáticamente.",
    )

    class Meta:
        model = Liquidaciones
        # No mostramos 'rut' porque se toma del trabajador
        fields = [
            "trabajador",
            "mes",
            "anio",
            "sbase",
            "sbruto",
            "desc_afp",
            "descuentos",
            "descuentos_totales",
            "sueldo_liquido",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si estamos editando una liquidación existente, pre-seleccionamos al trabajador
        if self.instance and self.instance.pk:
            trabajador = Trabajador.objects.filter(rut=self.instance.rut).first()
            if trabajador:
                self.fields["trabajador"].initial = trabajador

    # Aquí hacemos TODOS los cálculos de la pauta
    def clean(self):
        cleaned = super().clean()

        trabajador = cleaned.get("trabajador")
        mes = cleaned.get("mes")
        anio = cleaned.get("anio")

        # Si falta algo esencial, no calculamos
        if not trabajador or not mes or not anio:
            return cleaned

        # 1) rut desde el Trabajador
        cleaned["rut"] = trabajador.rut

        # 2) sbase = trabajador.base
        sbase = Decimal(trabajador.base or 0)
        cleaned["sbase"] = sbase

        # 3) sbruto = sbase
        sbruto = sbase
        cleaned["sbruto"] = sbruto

        # 4) desc_afp = sbase × (afp.descuento / 100)
        try:
            afp = Afps.objects.get(nombre=trabajador.afp)
            desc_afp = sbase * (Decimal(afp.descuento) / Decimal("100"))
        except Afps.DoesNotExist:
            desc_afp = Decimal("0")

        cleaned["desc_afp"] = desc_afp

        # 5) descuentos = suma de descuentos del trabajador (mismo RUT, mes y año)
        descuentos_qs = Descuentos.objects.filter(
            rut=trabajador.rut,
            fecha__year=anio,
            fecha__month=mes,
        )
        descuentos_sum = descuentos_qs.aggregate(total=Sum("monto"))["total"]
        if descuentos_sum is None:
            descuentos_sum = Decimal("0")

        cleaned["descuentos"] = descuentos_sum

        # 6) descuentos_totales = desc_afp + descuentos
        descuentos_totales = desc_afp + descuentos_sum
        cleaned["descuentos_totales"] = descuentos_totales

        # 7) sueldo_liquido = sbruto − descuentos_totales
        sueldo_liquido = sbruto - descuentos_totales
        cleaned["sueldo_liquido"] = sueldo_liquido

        return cleaned

    def save(self, commit=True):
        """
        Mantenemos tu lógica original:
        - Copiar el rut del trabajador a la instancia antes de guardar.
        Los montos ya vienen calculados desde clean().
        """
        trabajador = self.cleaned_data.get("trabajador")
        if trabajador:
            self.instance.rut = trabajador.rut
        return super().save(commit)
