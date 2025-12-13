from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("admin/", admin.site.urls),

    # LOGIN + DASHBOARDS
    path("", include("eva2LopezJorge_app.urls")),

    # API REST EVA3
    path("api/", include("Eva3Api.urls")),

    path("api-auth/", include("rest_framework.urls")),
    path("api/token/", obtain_auth_token, name="api_token"),
]
