from django.db import models

from apps.utils.base_model import UUIDBaseModel
from apps.utils.uploads import upload_path


class ProductCategory(UUIDBaseModel):
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
        """
        Returns a string representation of the full path of the product category.

        For example, if the product category structure is:
        A -> B -> C

        Then the full path of C is "A → B → C".
        """
        names = [self.name]
        p = self.parent
        while p:
            names.insert(0, p.name)
            p = p.parent
        return " → ".join(names)

    def __str__(self):
        return self.get_full_path()


class Product(UUIDBaseModel):
    sku = models.CharField("SKU", max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, blank=True
    )

    image = models.ImageField(upload_to=upload_path(), blank=True, null=True)

    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)

    stock_quantity = models.IntegerField(default=0)
    low_stock_alert = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    @property
    def is_low_stock(self) -> bool:
        """
        Determine if the product is in low stock.

        Returns:
            bool: True if the stock quantity is less than or equal to the low stock alert.
        """
        return self.stock_quantity <= self.low_stock_alert

    def __str__(self):
        return f"[{self.sku}] {self.name}" if self.sku else self.name
