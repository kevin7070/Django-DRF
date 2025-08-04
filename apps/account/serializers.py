from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

from .models import Company, CompanyRole, User


class UserSerializer(UserDetailsSerializer):
    phone = serializers.CharField(required=False)

    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class CompanyRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyRole
        fields = "__all__"
