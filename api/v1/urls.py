from django.urls import include, path

urlpatterns = [
    path("auth/", include("api.v1.auth.urls")),
    path("product/", include("api.v1.product.urls")),
]
