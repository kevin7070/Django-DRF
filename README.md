# Debian Package Requirements

- libpq-div
- python3-dev
- build-essential

# Requirements

- nvm or node
  - Node 18 or later
- pyenv or python
  - Python 3.11 or later

# Reference

### Generate secret key

```bash
openssl rand -base64 128 | tr -d '\n'
```

### To Install Python requirements

```bash
pip install -r requirements.txt
```

### To Generate requirements.txt

```bash
pip freeze > requirements.txt
```

### To Generate requirements-core.txt

```bash
pip list --not-required freeze > requirements-core.txt
```
