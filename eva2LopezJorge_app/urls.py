from django.urls import path
from .views import (
    login_view,
    logout_view,
    dashboard_admin,
    dashboard_trabajador,
    dashboard_jefe,
)

urlpatterns = [
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path("admin-dashboard/", dashboard_admin, name="dashboard_admin"),
    path("trabajador-dashboard/", dashboard_trabajador, name="dashboard_trabajador"),
    path("jefe-dashboard/", dashboard_jefe, name="dashboard_jefe"),
]

