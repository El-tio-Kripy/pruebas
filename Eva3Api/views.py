from datetime import datetime

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.settings import api_settings

from eva2Trabajador_app.models import Trabajador, Liquidaciones
from .serializers import TrabajadorSerializer, LiquidacionSerializer


class TokenProtectedAPIView(APIView):
    """Base común para exigir el mismo esquema de autenticación en todos los endpoints."""

    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES


class ApiHomeView(TokenProtectedAPIView):
    """Endpoint de prueba: confirma que la API está activa."""

    def get(self, request):
        return Response({"mensaje": "API Eva3 funcionando. Usa /api/trabajador/<rut>/"})


class TrabajadorDetailView(TokenProtectedAPIView):
    """EVA3 3.4.1: Datos personales del trabajador por RUT."""

    def get(self, request, rut):
        try:
            trabajador = Trabajador.objects.get(rut=rut)
        except Trabajador.DoesNotExist:
            return Response(
                {"error": "Trabajador no encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TrabajadorSerializer(trabajador)
        return Response(serializer.data)


class LiquidacionDetailView(TokenProtectedAPIView):
    """EVA3 3.4.2: Liquidación de un mes específico.
    GET /api/liquidacion/<rut>/<anio>/<mes>/
    """

    def get(self, request, rut, anio, mes):
        try:
            liq = Liquidaciones.objects.get(rut=rut, anio=anio, mes=mes)
        except Liquidaciones.DoesNotExist:
            return Response(
                {"error": "Liquidación no encontrada para el RUT y período indicado"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(LiquidacionSerializer(liq).data)


class LiquidacionHistorialView(TokenProtectedAPIView):
    """EVA3 3.4.3: Historial de liquidaciones de varios meses.
    GET /api/liquidacion/historial/<rut>/?desde=YYYY-MM&hasta=YYYY-MM
    """

    @staticmethod
    def _parse_yyyy_mm(value: str):
        # Formato esperado: '2024-01'
        return datetime.strptime(value, "%Y-%m").date()

    def get(self, request, rut):
        desde = request.query_params.get("desde")
        hasta = request.query_params.get("hasta")

        if not desde or not hasta:
            return Response(
                {"error": "Parámetros requeridos: desde=YYYY-MM y hasta=YYYY-MM"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            d = self._parse_yyyy_mm(desde)
            h = self._parse_yyyy_mm(hasta)
        except ValueError:
            return Response(
                {"error": "Formato inválido. Use desde=YYYY-MM y hasta=YYYY-MM"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (h.year, h.month) < (d.year, d.month):
            return Response(
                {"error": "Rango inválido: 'hasta' debe ser >= 'desde'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Filtro por rango (anio/mes) sin cambiar el modelo:
        qs = Liquidaciones.objects.filter(rut=rut).filter(
            Q(anio__gt=d.year) | Q(anio=d.year, mes__gte=d.month),
            Q(anio__lt=h.year) | Q(anio=h.year, mes__lte=h.month),
        ).order_by("anio", "mes")

        data = LiquidacionSerializer(qs, many=True).data
        return Response(
            {
                "rut": rut,
                "desde": desde,
                "hasta": hasta,
                "cantidad": len(data),
                "resultados": data,
            }
        )
