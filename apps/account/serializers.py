from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

from .models import Company, CompanyAddress, CompanyRole, User


class UserSerializer(UserDetailsSerializer):
    phone = serializers.CharField(required=False)

    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = "__all__"


class CompanyAddressBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAddress
        fields = (
            "id",
            "address",
            "apt_suite",
            "city",
            "province",
            "postal_code",
            "country",
            "is_mailing_address",
        )


class CompanySerializer(serializers.ModelSerializer):
    addresses = CompanyAddressBaseSerializer(many=True, read_only=True)
    mailing_address = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = (
            "id",
            "name",
            "verification_document",
            "is_verified",
            "verified",
            "verified_by",
            "addresses",
            "mailing_address",
        )

    def get_mailing_address(self, obj):
        mailing = obj.addresses.filter(is_mailing_address=True).first()
        if mailing:
            return CompanyAddressBaseSerializer(mailing).data
        return None


class CompanyRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyRole
        fields = ("id", "name", "permissions", "is_protected")
