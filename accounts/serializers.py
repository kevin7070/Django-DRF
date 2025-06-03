from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

from accounts.models import User


class CustomUserSerializer(UserDetailsSerializer):
    phone = serializers.CharField(required=False)

    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = (
            "id",
            "username",
            "email",
            "phone",
        )
