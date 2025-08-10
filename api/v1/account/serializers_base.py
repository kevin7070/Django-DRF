from rest_framework import serializers

from apps.account.models import Company, CompanyAddress, CompanyRole


class CompanyAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAddress
        fields = (
            "id",
            "company",
            "address",
            "apt_suite",
            "city",
            "province",
            "country",
            "postal_code",
            "is_mailing_address",
        )

    def validate(self, data):
        is_mailing = data.get("is_mailing_address", False)

        company = data.get("company")
        if not company and self.instance:
            company = self.instance.company

        if is_mailing and company:
            qs = CompanyAddress.objects.filter(
                company=company,
                is_mailing_address=True,
            )
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {
                        "is_mailing_address": "Only one mailing address is allowed per company."
                    }
                )

        return data


class CompanySerializer(serializers.ModelSerializer):
    addresses = CompanyAddressSerializer(many=True, read_only=True)
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
            return CompanyAddressSerializer(mailing).data
        return None


class CompanyRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyRole
        fields = ("id", "name", "permissions", "is_protected")
