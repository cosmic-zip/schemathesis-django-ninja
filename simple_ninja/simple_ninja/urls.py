from django.contrib import admin
from django.urls import path, include
from ninja import NinjaAPI
from allauth.headless.contrib.ninja.security import x_session_token_auth
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

api = NinjaAPI(
    auth=x_session_token_auth,
    docs_url="/docs/",
    openapi_url="/openapi.json",
)

api._original_get_openapi_schema = api.get_openapi_schema
_original_get_openapi_schema = api.get_openapi_schema


def patched_get_openapi_schema(request=None, path_params=None):
    schema = _original_get_openapi_schema()
    schema.setdefault("components", {}).setdefault("securitySchemes", {})[
        "XSessionTokenAuth"
    ] = {"type": "apiKey", "in": "header", "name": "X-Session-Token"}

    for path in schema.get("paths", {}).values():
        for op in path.values():
            if "security" not in op:
                op["security"] = [{"XSessionTokenAuth": []}]

    return schema


api.get_openapi_schema = patched_get_openapi_schema


@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}


urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("api/auth/allauth/", include("allauth.headless.urls")),
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("api/auth/allauth/openapi.json", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/auth/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
