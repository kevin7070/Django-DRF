# How To Run

## 1. Create a .env file in the root directory

```bash
# DJANGO_ENVIRONMENT=production
DJANGO_ENVIRONMENT=development

# Secret Keys
JWT_SIGNING_KEY="your-really-secure-secret"
DJANGO_SECRET_KEY="your-really-secure-secret"

# Django hosts, use comma to separate
DJANGO_ALLOWED_HOSTS="api.example.com, www.api.example.com, localhost, 127.0.0.1"

# Postgresql Data
POSTGRES_DB=""
POSTGRES_USER=""
POSTGRES_PASSWORD=""
POSTGRES_HOST="127.0.0.1"
POSTGRES_PORT="5432"

# Frontend domains, use comma to separate, add Django hosts for admin panel
FRONTEND_DOMAINS="https://example.com, https://www.example.com, https://api.example.com, https://www.api.example.com, http://localhost:3000, http://127.0.0.1:3000"

# Django Admin Path to exposing in URL, keep it empty to default `/admin/`
DJANGO_ADMIN_PATH=supersecret
```

## 2. Install Requirements

### Database Configuration (PostgreSQL by Default)

This project is currently configured to use **PostgreSQL**.
If you prefer to use another database, such as **MariaDB** or others, feel free to update the settings under the `config/settings` folder.

[Read more in the Django documentation.](https://docs.djangoproject.com/en/5.2/ref/databases/)

OS Package required to build "psycopg2"

**Debian 12**

- libpq-div
- python3-dev
- build-essential

**Fedora 42**

- libpq-devel
- python3-devel

### Environment

- [ nvm ](https://github.com/nvm-sh/nvm) or [ node ](https://nodejs.org/en)
  - version 18 or later
- [ pyenv ](https://github.com/pyenv/pyenv) or [ python ](https://www.python.org/)
  - version 3.11 or later

### Dependencies

_install in your python environment_

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.lock.txt
```

## 3. Run

```bash
cd [path/to/project/root]
python manage.py runserver
```

> Official Documentation:
> [ Devemopment ](https://docs.djangoproject.com/en/5.2/intro/tutorial01/)
> and
> [ Production ](https://docs.djangoproject.com/en/5.1/howto/deployment/)

# Reference

### Generate your own secret key

```bash
openssl rand -base64 128 | tr -d '\n'
```

# Upgrade

### Python package

```bash
pip-compile requirements.in --upgrade
pip install -r requirements.txt
```

### Tests and Checks

```bash
python manage.py check
python manage.py test
```

### Stage to lock file

```bash
pip freeze > requirements.lock.txt
```
