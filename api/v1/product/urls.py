from django.urls import path

from .views import ProductCategoryTreeView

urlpatterns = [
    path("categories/tree/", ProductCategoryTreeView.as_view()),
]
