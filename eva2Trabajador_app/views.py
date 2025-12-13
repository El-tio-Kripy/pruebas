from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse

from .models import Liquidaciones


def listado_liquidaciones(request):
    hoy = timezone.now()
    mes = hoy.month
    anio = hoy.year
    liquidaciones = Liquidaciones.objects.filter(mes=mes, anio=anio)

    contexto = {
        "liquidaciones": liquidaciones,
        "mes": mes,
        "anio": anio,
    }
    return render(request, "eva2Trabajador_app/listado_liquidaciones.html", contexto)


def api_liquidaciones(request):
    liquidaciones = Liquidaciones.objects.all()

    data = []
    for liq in liquidaciones:
        data.append({
            "trabajador_rut": liq.trabajador.rut,
            "trabajador_nombre": liq.trabajador.nombre,
            "mes": liq.mes,
            "anio": liq.anio,
            "sueldo_base": liq.sbase,
            "sueldo_bruto": liq.sbruto,
            "desc_afp": liq.desc_afp,
            "descuentos": liq.descuentos,
            "descuentos_totales": liq.descuentos_totales,
            "sueldo_liquido": liq.sueldo_liquido,
        })

    return JsonResponse(data, safe=False)
