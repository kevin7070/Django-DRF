from rest_framework import serializers

from apps.account.serializers import CompanyAddress, CompanyAddressBaseSerializer


class CompanyAddressSerializer(CompanyAddressBaseSerializer):
    def validate(self, data):
        is_mailing = data.get("is_mailing_address", False)
        company = (
            data.get("company") or self.instance.company if self.instance else None
        )

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
