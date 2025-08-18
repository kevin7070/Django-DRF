from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from apps.utils.files import delete_file_field

from .models import Company, User


@receiver(post_delete, sender=User)
def user_profile_picture_cleanup(sender, instance, **kwargs):
    delete_file_field(getattr(instance, "profile_picture", None))


@receiver(pre_save, sender=User)
def user_profile_picture_replace(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    old_f = getattr(old, "profile_picture", None)
    new_f = getattr(instance, "profile_picture", None)
    if old_f and old_f.name and (not new_f or old_f.name != new_f.name):
        delete_file_field(old_f)


@receiver(post_delete, sender=Company)
def company_verification_doc_cleanup(sender, instance, **kwargs):
    delete_file_field(getattr(instance, "verification_document", None))


@receiver(pre_save, sender=Company)
def company_verification_doc_replace(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    old_f = getattr(old, "verification_document", None)
    new_f = getattr(instance, "verification_document", None)
    if old_f and old_f.name and (not new_f or old_f.name != new_f.name):
        delete_file_field(old_f)
