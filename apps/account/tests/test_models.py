import pytest

from apps.account.models import Company, CompanyAddress, CompanyRole, User


@pytest.mark.django_db
def test_create_user_requires_username_and_email_and_password():
    with pytest.raises(ValueError):
        User.objects.create_user(
            username="",
            email="user@helloworld.ca",
            password="passwd",
        )
    with pytest.raises(ValueError):
        User.objects.create_user(
            username="user",
            email="",
            password="passwd",
        )
    with pytest.raises(ValueError):
        User.objects.create_user(
            username="user",
            email="user@helloworld.ca",
            password="",
        )


@pytest.mark.django_db
def test_create_superuser_requires_staff_and_superuser():
    with pytest.raises(ValueError):
        User.objects.create_superuser(
            username="admin",
            email="admin@helloworld.ca",
            password="passwd",
            is_staff=False,
        )
    with pytest.raises(ValueError):
        User.objects.create_superuser(
            username="admin",
            email="admin@helloworld.ca",
            password="passwd",
            is_superuser=False,
        )


@pytest.mark.django_db
def test_create_company():
    company = Company.objects.create(name="Test Corp")
    assert company.name == "Test Corp"
    assert company.is_verified is False


@pytest.mark.django_db
def test_company_address_full_address():
    company = Company.objects.create(name="Test Co")
    addr = CompanyAddress.objects.create(
        company=company,
        address="123 Main St",
        apt_suite="5B",
        city="Toronto",
        province="ON",
        postal_code="M1A1A1",
        country="Canada",
        is_mailing_address=True,
    )
    assert "123 Main St" in addr.full_address
    assert "Unit 5B" in addr.full_address
    assert "Toronto" in addr.full_address


@pytest.mark.django_db
def test_company_role_permission_check():
    company = Company.objects.create(name="Perm Co")
    role = CompanyRole.objects.create(
        company=company,
        name="Editor",
        permissions={
            "product": {"update": True, "delete": False},
            "invoice": {"read": True},
        },
    )
    assert role.has_perm("product", "update") is True
    assert role.has_perm("product", "delete") is False
    assert role.has_perm("invoice", "read") is True
    assert role.has_perm("missing_module", "update") is False


@pytest.mark.django_db
def test_create_user():
    company = Company.objects.create(name="User Co")
    role = CompanyRole.objects.create(company=company, name="Admin")
    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="pass1234",
        company=company,
        company_role=role,
    )
    assert user.username == "testuser"
    assert user.check_password("pass1234")
    assert user.company == company
    assert user.company_role == role
