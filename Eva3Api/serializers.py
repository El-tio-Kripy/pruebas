from rest_framework import serializers
from eva2Trabajador_app.models import Trabajador, Liquidaciones


class TrabajadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajador
        fields = ["rut", "nombre", "base", "afp"]


class LiquidacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liquidaciones
        # Campos definidos en la pauta EVA3 (tabla liquidaciones)
        fields = [
            "rut",
            "mes",
            "anio",
            "sbase",
            "sbruto",
            "desc_afp",
            "descuentos",
            "descuentos_totales",
            "sueldo_liquido",
        ]
