from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.product.models import ProductCategory

from .serializers import ProductCategoryTreeSerializer


class ProductCategoryTreeView(APIView):
    permission_classes = [AllowAny]  # TODO: for testing, to be removed

    def get(self, request):
        roots = ProductCategory.objects.filter(parent__isnull=True).order_by("name")
        data = ProductCategoryTreeSerializer(roots, many=True).data
        return Response(data)
