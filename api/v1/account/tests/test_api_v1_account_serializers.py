import pytest
from api.v1.account.serializers import UserSerializer
from api.v1.account.serializers_base import CompanyAddressSerializer
from apps.account.models import Company, CompanyAddress, User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.exceptions import ValidationError


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


@pytest.mark.django_db
def test_user_serializer_includes_expected_fields():
    user = User.objects.create_user(
        email="hello@world.ca",
        password="pass1234",
        username="helloworld",
        mobile="222-222-2222",
    )

    serializer = UserSerializer(instance=user)
    data = serializer.data

    # Fields from dj_rest_auth.UserDetailsSerializer are typically:
    # ("pk", "username", "email", "first_name", "last_name")
    # Our subclass adds: mobile, profile_picture
    for key in [
        "pk",
        "username",
        "email",
        "first_name",
        "last_name",
        "mobile",
        "profile_picture",
    ]:
        assert key in data, (
            f"Missing field: {key} in serialized data: {list(data.keys())}"
        )


@pytest.mark.django_db
def test_user_serializer_relations_are_primary_keys():
    # Company relations moved to memberships; ensure serializer still works without them
    user = User.objects.create_user(
        email="hello@world.ca",
        password="pass1234",
        username="helloworld",
    )
    serializer = UserSerializer(instance=user)
    data = serializer.data
    assert data["pk"] == str(user.pk) or data["pk"] == user.pk
    assert data["email"] == "hello@world.ca"


@pytest.mark.django_db
def test_user_serializer_profile_picture_serializes_path_when_present():
    pic = SimpleUploadedFile("avatar.png", b"fakepngbytes", content_type="image/png")

    user = User.objects.create_user(
        email="hello@world.ca",
        password="pass1234",
        username="helloworld",
        profile_picture=pic,
    )

    serializer = UserSerializer(instance=user)
    data = serializer.data

    # DRF returns a URL or path string for ImageField depending on storage
    assert data["profile_picture"], (
        "Expected profile_picture to be a non-empty string when set"
    )
