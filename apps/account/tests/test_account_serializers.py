import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.account.models import Company, CompanyRole, User
from apps.account.serializers import UserSerializer


@pytest.mark.django_db
def test_user_serializer_includes_expected_fields():
    company = Company.objects.create(name="HandyMan")
    role = CompanyRole.objects.create(company=company, name="admin")

    user = User.objects.create_user(
        username="helloworld",
        email="hello@world.ca",
        password="pass1234",
        phone="111-111-1111",
        mobile="222-222-2222",
        company=company,
        company_role=role,
    )

    serializer = UserSerializer(instance=user)
    data = serializer.data

    # Fields from dj_rest_auth.UserDetailsSerializer are typically:
    # ("pk", "username", "email", "first_name", "last_name")
    # Our subclass adds: company, company_role, phone, mobile, profile_picture
    for key in [
        "pk",
        "username",
        "email",
        "first_name",
        "last_name",
        "company",
        "company_role",
        "phone",
        "mobile",
        "profile_picture",
    ]:
        assert key in data, (
            f"Missing field: {key} in serialized data: {list(data.keys())}"
        )


@pytest.mark.django_db
def test_user_serializer_relations_are_primary_keys():
    company = Company.objects.create(name="HandyMan")
    role = CompanyRole.objects.create(company=company, name="staff")
    user = User.objects.create_user(
        username="helloworld",
        email="hello@world.ca",
        password="pass1234",
        company=company,
        company_role=role,
    )

    serializer = UserSerializer(instance=user)
    data = serializer.data

    assert data["company"] == str(company.pk) or data["company"] == company.pk
    assert data["company_role"] == str(role.pk) or data["company_role"] == role.pk


@pytest.mark.django_db
def test_user_serializer_phone_is_not_required_on_input():
    company = Company.objects.create(name="HandyMan")
    role = CompanyRole.objects.create(company=company, name="user")

    # Prepare payload similar to what the serializer would accept for updates
    payload = {
        "username": "",
        "email": "hello@world.ca",
        "first_name": "hello",
        "last_name": "world",
        # phone omitted on purpose
        "mobile": "111-111-1111",
        "company": str(company.pk),
        "company_role": str(role.pk),
    }

    # Initialize for creation/update-like validation (no instance)
    serializer = UserSerializer(data=payload)
    # UserDetailsSerializer usually does partial updates; allow partial to avoid requiring all default fields
    assert serializer.is_valid(raise_exception=True) is True


@pytest.mark.django_db
def test_user_serializer_profile_picture_serializes_path_when_present():
    company = Company.objects.create(name="HandyMan")
    role = CompanyRole.objects.create(company=company, name="uploader")

    pic = SimpleUploadedFile("avatar.png", b"fakepngbytes", content_type="image/png")

    user = User.objects.create_user(
        username="helloworld",
        email="hello@world.ca",
        password="pass1234",
        company=company,
        company_role=role,
        profile_picture=pic,
    )

    serializer = UserSerializer(instance=user)
    data = serializer.data

    # DRF returns a URL or path string for ImageField depending on storage
    assert data["profile_picture"], (
        "Expected profile_picture to be a non-empty string when set"
    )
