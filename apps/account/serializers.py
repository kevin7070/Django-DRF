from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

from .models import User


class UserSerializer(UserDetailsSerializer):
    phone = serializers.CharField(required=False)

    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = "__all__"
