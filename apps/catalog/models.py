from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from apps.stores.models import Store
import uuid

def category_image_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"stores/{instance.store.slug}/categories/{uuid.uuid4()}.{ext}"

class Category(models.Model):

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="categories"
    )

    name = models.CharField(max_length=120)

    slug = models.SlugField(
        max_length=140,
        blank=True
    )

    image = models.ImageField(
        upload_to=category_image_path,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["store", "slug"],
                name="unique_category_slug_per_store"
            )
        ]

    def save(self, *args, **kwargs):

        if not self.slug:
            base_slug = slugify(self.name)

            slug = base_slug
            counter = 1

            while Category.objects.filter(
                store=self.store,
                slug=slug
            ).exclude(pk=self.pk).exists():

                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.store.name} - {self.name}"
    
def product_image_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"stores/{instance.store.slug}/products/{uuid.uuid4()}.{ext}"

def generate_unique_slug(instance):
    base_slug = slugify(instance.name)
    slug = base_slug
    num = 1
    while Product.objects.filter(store=instance.store, slug=slug).exists():
        slug = f"{base_slug}-{num}"
        num += 1
        if num > 1000:  # fallback, raro que pase
            slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
            break
    return slug

class Product(models.Model):

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="products"
    )

    category = models.ForeignKey(
        "catalog.Category",
        on_delete=models.PROTECT,
        related_name="products"
    )

    name = models.CharField(max_length=150)

    slug = models.SlugField(
        max_length=160,
        blank=True
    )

    description = models.TextField(blank=True)

    image = models.ImageField(
        upload_to=product_image_path,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["store", "slug"],
                name="unique_product_slug_per_store"
            )
        ]

    def clean(self):
        if self.category and self.category.store != self.store:
            raise ValidationError(
                "La categoría no pertenece a esta tienda."
            )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self)
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.store.name} - {self.name}"

class ProductVariant(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants"
    )

    name = models.CharField(
        max_length=120,
        help_text="Ej: 250g, 500g, Talla M"
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=0
    )

    min_order_quantity = models.PositiveIntegerField(
        default=1,
        help_text="Cantidad mínima para compra mayorista"
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "name"],
                name="unique_variant_per_product"
            )
        ]

    def save(self, *args, **kwargs):
        self.name = self.name.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.name}"