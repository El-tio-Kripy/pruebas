from django.urls import path
from .views import (
    ApiHomeView,
    TrabajadorDetailView,
    LiquidacionDetailView,
    LiquidacionHistorialView,
)

urlpatterns = [
    # El proyecto ya incluye este módulo bajo el prefijo /api/
    path("", ApiHomeView.as_view(), name="api_home"),
    # EVA3 3.4.1 -> /api/trabajador/<rut>/
    path("trabajador/<str:rut>/", TrabajadorDetailView.as_view(), name="trabajador_detail"),
    # EVA3 3.4.2 -> /api/liquidacion/<rut>/<anio>/<mes>/
    path(
        "liquidacion/<str:rut>/<int:anio>/<int:mes>/",
        LiquidacionDetailView.as_view(),
        name="liquidacion_detail",
    ),
    # EVA3 3.4.3 -> /api/liquidacion/historial/<rut>/?desde=YYYY-MM&hasta=YYYY-MM
    path(
        "liquidacion/historial/<str:rut>/",
        LiquidacionHistorialView.as_view(),
        name="liquidacion_historial",
    ),
]
