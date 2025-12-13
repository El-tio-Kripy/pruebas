from datetime import date
import hashlib

from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Usuarios
from .forms import LoginForm

from eva2Trabajador_app.models import Trabajador, Liquidaciones, Descuentos


# -----------------------------------------------------------
# LOGIN
# -----------------------------------------------------------
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # Buscar usuario
            try:
                usuario = Usuarios.objects.get(username=username)
            except Usuarios.DoesNotExist:
                messages.error(request, "Usuario no registrado")
                return redirect("login")

            # Comparar contraseñas usando HASH SHA256 (coherente con el modelo)
            hash_ingresado = hashlib.sha256(password.encode("utf-8")).hexdigest()
            if hash_ingresado != usuario.hash:
                messages.error(request, "Credenciales incorrectas")
                return redirect("login")

            # Guardar sesión
            request.session["usuario_id"] = usuario.id
            request.session["perfil"] = usuario.perfil
            request.session["nombre"] = usuario.nombre
            request.session["username"] = usuario.username

            # Redirigir según perfil
            if usuario.perfil == Usuarios.PERFIL_ADMIN:
                return redirect("dashboard_admin")

            if usuario.perfil == Usuarios.PERFIL_TRABAJADOR:
                return redirect("dashboard_trabajador")

            if usuario.perfil == Usuarios.PERFIL_JEFE:
                return redirect("dashboard_jefe")

    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


# -----------------------------------------------------------
# LOGOUT
# -----------------------------------------------------------
def logout_view(request):
    request.session.flush()
    return redirect("login")


# -----------------------------------------------------------
# DASHBOARD ADMIN
# -----------------------------------------------------------
def dashboard_admin(request):
    if request.session.get("perfil") != 1:
        return redirect("login")

    return render(request, "dashboard_admin.html")


# -----------------------------------------------------------
# DASHBOARD TRABAJADOR
# -----------------------------------------------------------
def dashboard_trabajador(request):
    if request.session.get("perfil") != 2:
        return redirect("login")

    rut = request.session.get("username", "")
    hoy = date.today()

    # Buscar trabajador por rut
    try:
        trabajador = Trabajador.objects.get(rut=rut)
    except Trabajador.DoesNotExist:
        return render(
            request,
            "dashboard_trabajador.html",
            {"error": "Trabajador no encontrado"},
        )

    # Liquidación del mes
    liquidacion = Liquidaciones.objects.filter(
        rut=rut,
        mes=hoy.month,
        anio=hoy.year,
    ).first()

    descuentos = Descuentos.objects.filter(
        rut=rut,
        fecha__year=hoy.year,
        fecha__month=hoy.month,
    )

    contexto = {
        "trabajador": trabajador,
        "liquidacion": liquidacion,
        "descuentos": descuentos,
    }

    return render(request, "dashboard_trabajador.html", contexto)


# -----------------------------------------------------------
# DASHBOARD JEFE
# -----------------------------------------------------------
def dashboard_jefe(request):
    if request.session.get("perfil") != 3:
        return redirect("login")

    liquidaciones = Liquidaciones.objects.all().order_by("-anio", "-mes")

    return render(request, "dashboard_jefe.html", {"liquidaciones": liquidaciones})
