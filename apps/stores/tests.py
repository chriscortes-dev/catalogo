from django.test import TestCase
from django.urls import reverse

from apps.catalog.models import Category, Product, ProductVariant
from apps.stores.models import Store


class StoreRoutingTests(TestCase):

    def setUp(self):
        self.store = Store.objects.create(
            name="Mi Tienda",
            whatsapp_number="56912345678",
        )

    def test_store_landing_renders_by_slug(self):
        url = reverse("store_landing", args=[self.store.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "stores/landing.html")

    def test_home_renders_marketing_landing(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "marketing_landing.html")

    def test_unknown_store_slug_returns_404(self):
        response = self.client.get("/tienda-inexistente/")
        self.assertEqual(response.status_code, 404)

    def test_inactive_store_returns_404(self):
        self.store.is_active = False
        self.store.save()
        response = self.client.get(
            reverse("store_landing", args=[self.store.slug])
        )
        self.assertEqual(response.status_code, 404)

    def test_catalog_and_product_detail_are_scoped_to_store(self):
        category = Category.objects.create(
            store=self.store,
            name="Café",
        )
        product = Product.objects.create(
            store=self.store,
            category=category,
            name="Café de grano",
        )
        ProductVariant.objects.create(
            product=product,
            name="500g",
            price=10000,
        )

        catalog_url = reverse(
            "catalog",
            args=[self.store.slug, category.slug],
        )
        response = self.client.get(catalog_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/catalog.html")

        product_url = reverse(
            "product_detail",
            args=[self.store.slug, category.slug, product.slug],
        )
        response = self.client.get(product_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/product_detail.html")
