from rest_framework import serializers

from apps.product.serializers import (
    ProductCategorySerializer as BaseProductCategorySerializer,
)


class ProductCategoryTreeSerializer(BaseProductCategorySerializer):
    full_path = serializers.SerializerMethodField()
    has_children = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta(BaseProductCategorySerializer.Meta):
        fields = ("id", "name", "full_path", "has_children", "children")

    def get_full_path(self, obj) -> str:
        return obj.get_full_path()

    def get_has_children(self, obj) -> bool:
        return obj.children.exists()

    def get_children(self, obj) -> list:
        return ProductCategoryTreeSerializer(obj.children.all(), many=True).data
