from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from apps.product.models import Product
from apps.utils.files import delete_file_field


@receiver(post_delete, sender=Product)
def delete_product_image_on_delete(sender, instance, **kwargs):
    delete_file_field(instance.image)


@receiver(pre_save, sender=Product)
def delete_product_image_on_change(sender, instance, Product, **kwargs):
    if not instance.pk:
        return
    try:
        old = Product.objects.get(pk=instance.pk)
    except Product.DoesNotExist:
        return
    old_f = getattr(old, "image", None)
    new_f = getattr(instance, "image", None)
    if old_f and old_f.name and (not new_f or old_f.name != new_f.name):
        delete_file_field(old_f)
