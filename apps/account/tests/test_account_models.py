import pytest
from apps.account.models import Company, CompanyRole, User


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
@pytest.mark.parametrize(
    "module,action,expected",
    [
        ("product", "read", True),
        ("product", "create", False),
        ("product", "update", False),
        ("product", "delete", False),
        ("missing_module", "read", False),
        ("missing_module", "create", False),
        ("missing_module", "update", False),
        ("missing_module", "delete", False),
    ],
)
def test_company_role_permission_check(module, action, expected):
    company = Company.objects.create(name="Perm Co")
    role = CompanyRole.objects.create(
        company=company,
        name="Editor",
    )
    assert role.has_perm(module, action) is expected
