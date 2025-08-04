import os

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.utils.base_model import UUIDTimestampModel


class ProductCategory(UUIDTimestampModel):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"
        unique_together = ("name", "parent")

    def get_full_path(self):
        names = [self.name]
        p = self.parent
        while p:
            names.insert(0, p.name)
            p = p.parent
        return " → ".join(names)

    def __str__(self):
        return self.get_full_path()


class Product(UUIDTimestampModel):
    sku = models.CharField("SKU", max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, blank=True
    )

    image = models.ImageField(
        upload_to="apps/product/images/%Y/%m/", blank=True, null=True
    )

    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)

    stock_quantity = models.IntegerField(default=0)
    low_stock_alert = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"[{self.sku}] {self.name}" if self.sku else self.name

    @property
    def is_low_stock(self) -> bool:
        return self.stock_quantity <= self.low_stock_alert


@receiver(post_delete, sender=Product)
def delete_product_image(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path
        if os.path.isfile(image_path):
            instance.image.delete(save=False)
