from pathlib import Path
from uuid import uuid4

from django.utils import timezone
from django.utils.deconstruct import deconstructible


@deconstructible
class UploadPath:
    def __init__(self, use_day: bool = True):
        self.use_day = use_day

    def __call__(self, instance, filename: str) -> str:
        app_label = instance._meta.app_label
        model_name = instance._meta.model_name
        ext = Path(filename).suffix.lower()
        now = timezone.now()
        date = now.strftime("%Y/%m/%d") if self.use_day else now.strftime("%Y/%m")
        return f"Uploads/{app_label}/{model_name}/{date}/{uuid4().hex}{ext}"


# Utility: Use for better readability (avoiding functools.partial/closure migration issues)
def upload_path(*, use_day: bool = True) -> UploadPath:
    """
    Creates an instance of UploadPath with the specified use_day option.

    :param use_day: If True, the date will be divided into day-level directories.
                    Otherwise, it will be divided into month-level directories.
    :type use_day: bool

    :return: An instance of UploadPath.
    :rtype: UploadPath
    """
    return UploadPath(use_day=use_day)
