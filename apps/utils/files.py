from typing import Optional

from django.db.models.fields.files import FieldFile


def delete_file_field(f: Optional[FieldFile]) -> None:
    if not f or not getattr(f, "name", None):
        return
    try:
        storage = f.storage
        if storage.exists(f.name):
            storage.delete(f.name)
    except Exception:
        pass
