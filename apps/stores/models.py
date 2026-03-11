from django.db import models
from django.utils.text import slugify
import uuid

def store_logo_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"stores/{instance.slug}/logos/{uuid.uuid4()}.{ext}"

def generate_unique_store_slug(instance):
    base_slug = slugify(instance.name)
    slug = base_slug
    num = 1
    while Store.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{num}"
        num += 1
        if num > 1000:  # fallback raro
            slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
            break
    return slug

class Store(models.Model):

    # Identidad
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)

    # Contacto
    whatsapp_number = models.CharField(max_length=20)

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    address = models.CharField(
        max_length=255,
        blank=True
    )

    # Redes
    instagram_username = models.CharField(
        max_length=50,
        blank=True
    )

    # Branding
    logo = models.ImageField(
        upload_to=store_logo_path,
        blank=True
    )

    # Landing comercial
    hero_title = models.CharField(
        max_length=255,
        blank=True
    )

    hero_subtitle = models.CharField(
        max_length=255,
        blank=True
    )

    # Estado
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_store_slug(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name