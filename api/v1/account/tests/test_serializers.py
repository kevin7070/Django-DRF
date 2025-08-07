import pytest
from rest_framework.exceptions import ValidationError

from api.v1.account.serializers import CompanyAddressSerializer
from apps.account.models import Company, CompanyAddress


@pytest.mark.django_db
def test_create_first_mailing_address():
    company = Company.objects.create(name="Google Toronto")
    data = {
        "company": company.id,
        "address": "111 Richmond St W",
        "apt_suite": "",
        "city": "Toronto",
        "province": "ON",
        "country": "Canada",
        "postal_code": "M5H 2G4",
        "is_mailing_address": True,
    }
    serializer = CompanyAddressSerializer(data=data)
    assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db
def test_reject_duplicate_mailing_address():
    company = Company.objects.create(name="Google Toronto")
    CompanyAddress.objects.create(
        company=company,
        address="111 Richmond St W",
        apt_suite="",
        city="Toronto",
        province="ON",
        country="Canada",
        postal_code="M5H 2G4",
        is_mailing_address=True,
    )

    # create another one
    data = {
        "company": company.id,
        "address": "1 Richmond St W",
        "apt_suite": "",
        "city": "Toronto",
        "province": "ON",
        "country": "Canada",
        "postal_code": "M5H 2G4",
        "is_mailing_address": True,
    }

    serializer = CompanyAddressSerializer(data=data)
    with pytest.raises(ValidationError) as exc:
        serializer.is_valid(raise_exception=True)
    assert "Only one mailing address is allowed per company." in str(exc.value)


@pytest.mark.django_db
def test_allow_update_same_instance():
    company = Company.objects.create(name="Google Toronto")
    instance = CompanyAddress.objects.create(
        company=company,
        address="111 Richmond St W",
        apt_suite="",
        city="Toronto",
        province="ON",
        country="Canada",
        postal_code="M5H 2G4",
        is_mailing_address=True,
    )

    # update the same instance
    data = {
        "company": company.id,
        "address": "1 Richmond St W",
        "apt_suite": "",
        "city": "Toronto",
        "province": "ON",
        "country": "Canada",
        "postal_code": "M5H 2G4",
        "is_mailing_address": True,
    }

    serializer = CompanyAddressSerializer(instance=instance, data=data)
    assert serializer.is_valid(), serializer.errors
