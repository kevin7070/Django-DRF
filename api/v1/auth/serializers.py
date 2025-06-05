from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # User get_user_model explicitly
        fields = ("pk", "username", "email", "phone")
        read_only_fields = ("pk", "username", "email")
