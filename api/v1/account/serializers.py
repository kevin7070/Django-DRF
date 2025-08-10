from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

from apps.account.models import User


class UserSerializer(UserDetailsSerializer):
    phone = serializers.CharField(required=False)

    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = UserDetailsSerializer.Meta.fields + (
            "company",
            "company_role",
            "phone",
            "mobile",
            "profile_picture",
        )

    def get_fields(self):
        fields = super().get_fields()
        # Always expose a read-only username field
        if "username" not in fields:
            fields["username"] = serializers.CharField(read_only=True)
        return fields

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if "username" not in data:
            data["username"] = (
                getattr(instance, "username", None) or instance.get_username()
            )
        return data
