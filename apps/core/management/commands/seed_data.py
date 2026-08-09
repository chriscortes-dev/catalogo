from django.core.management.base import BaseCommand

from apps.catalog.models import Category, Product, ProductVariant
from apps.stores.models import Store


def make_store(data):
    store, created = Store.objects.update_or_create(
        slug=data["slug"],
        defaults={
            "name": data["name"],
            "whatsapp_number": data["whatsapp_number"],
            "hero_title": data["hero_title"],
            "hero_subtitle": data["hero_subtitle"],
            "is_active": True,
        },
    )
    return store, created


def make_category(store, name, slug):
    category, created = Category.objects.get_or_create(
        store=store,
        slug=slug,
        defaults={"name": name, "is_active": True},
    )
    return category, created


def make_product(store, category, name, slug, description, variants):
    product, created = Product.objects.get_or_create(
        store=store,
        slug=slug,
        defaults={
            "category": category,
            "name": name,
            "description": description,
            "is_active": True,
        },
    )
    if not created:
        product.category = category
        product.name = name
        product.description = description
        product.save()

    for variant_name, price, min_order in variants:
        ProductVariant.objects.get_or_create(
            product=product,
            name=variant_name,
            defaults={"price": price, "min_order_quantity": min_order},
        )

    return product, created


CATALOG = [
    {
        "name": "Café Montaña",
        "slug": "cafe-montana",
        "whatsapp_number": "56911112222",
        "hero_title": "Café de especialidad al por mayor",
        "hero_subtitle": "Grano de altura tostado en Chile, precios mayoristas desde 1 kg.",
        "categories": [
            {
                "name": "Café en grano",
                "slug": "cafe-en-grano",
                "products": [
                    {
                        "name": "Café Arábica Reserva",
                        "slug": "cafe-arabica-reserva",
                        "description": "Arábica de la zona de Los Ríos, notas a chocolate y frutos rojos.",
                        "variants": [
                            ("1kg", 14000, 1),
                            ("5kg", 65000, 2),
                            ("10kg", 120000, 5),
                        ],
                    },
                    {
                        "name": "Café Tostado Oscuro",
                        "slug": "cafe-tostado-oscuro",
                        "description": "Tostado largo, cuerpo intenso, ideal para espresso.",
                        "variants": [
                            ("1kg", 12000, 1),
                            ("5kg", 55000, 2),
                        ],
                    },
                ],
            },
            {
                "name": "Café molido",
                "slug": "cafe-molido",
                "products": [
                    {
                        "name": "Café Molido Fino",
                        "slug": "cafe-molido-fino",
                        "description": "Molido medio, listo para cafetera de filtro.",
                        "variants": [
                            ("500g", 7000, 1),
                            ("1kg", 13000, 1),
                        ],
                    },
                ],
            },
            {
                "name": "Accesorios",
                "slug": "accesorios",
                "products": [
                    {
                        "name": "V60 Cerámica",
                        "slug": "v60-ceramica",
                        "description": "Pour over de cerámica color mate.",
                        "variants": [
                            ("Unidad", 9000, 6),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "name": "Panadería La Espiga",
        "slug": "panaderia-la-espiga",
        "whatsapp_number": "56922223333",
        "hero_title": "Pan artesanal para tu local",
        "hero_subtitle": "Elaborado a diario con masa madre. Entrega a tu negocio.",
        "categories": [
            {
                "name": "Panes",
                "slug": "panes",
                "products": [
                    {
                        "name": "Pan de masa madre",
                        "slug": "pan-masa-madre",
                        "description": "Pan campesino de 800g, corteza crujiente y miga húmeda.",
                        "variants": [
                            ("Unidad", 3500, 10),
                            ("Caja x12", 38000, 10),
                        ],
                    },
                    {
                        "name": "Marraqueta",
                        "slug": "marraqueta",
                        "description": "La clásica marraqueta chilena, crujiente por fuera.",
                        "variants": [
                            ("Bolsa x10", 2500, 20),
                        ],
                    },
                ],
            },
            {
                "name": "Repostería",
                "slug": "reposteria",
                "products": [
                    {
                        "name": "Berlín",
                        "slug": "berlin",
                        "description": "Berlín relleno de crema pastelera.",
                        "variants": [
                            ("Unidad", 1200, 12),
                            ("Docena", 13000, 12),
                        ],
                    },
                ],
            },
            {
                "name": "Pasteles",
                "slug": "pasteles",
                "products": [
                    {
                        "name": "Torta Milhojas",
                        "slug": "torta-milhojas",
                        "description": "Torta de hojarasca y crema, por pedido.",
                        "variants": [
                            ("8 porciones", 18000, 1),
                            ("16 porciones", 32000, 1),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "name": "Distribuidora Norte",
        "slug": "distribuidora-norte",
        "whatsapp_number": "56933334444",
        "hero_title": "Abarrotes para minimarkets",
        "hero_subtitle": "Stock mayorista con despacho a la región.",
        "categories": [
            {
                "name": "Abarrotes",
                "slug": "abarrotes",
                "products": [
                    {
                        "name": "Arroz Grado 1",
                        "slug": "arroz-grado-1",
                        "description": "Arroz largo grado 1, bolsa de 25 kg.",
                        "variants": [
                            ("Saco 25kg", 28000, 2),
                        ],
                    },
                    {
                        "name": "Aceite Vegetal",
                        "slug": "aceite-vegetal",
                        "description": "Botella de 900 ml, marca propia.",
                        "variants": [
                            ("Caja x12", 18000, 6),
                        ],
                    },
                ],
            },
            {
                "name": "Lácteos",
                "slug": "lacteos",
                "products": [
                    {
                        "name": "Leche Entera",
                        "slug": "leche-entera",
                        "description": "Leche en polvo entera, tarro de 400g.",
                        "variants": [
                            ("Tarro", 3500, 24),
                        ],
                    },
                ],
            },
            {
                "name": "Congelados",
                "slug": "congelados",
                "products": [
                    {
                        "name": "Papas Prefritas",
                        "slug": "papas-prefritas",
                        "description": "Papas prefritas congeladas, bolsa de 2.5 kg.",
                        "variants": [
                            ("Bolsa 2.5kg", 8000, 4),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "name": "Mercado Verde",
        "slug": "mercado-verde",
        "whatsapp_number": "56944445555",
        "hero_title": "Frutas y verduras orgánicas",
        "hero_subtitle": "Del huerto a tu negocio, sin intermediarios.",
        "categories": [
            {
                "name": "Frutas y verduras",
                "slug": "frutas-y-verduras",
                "products": [
                    {
                        "name": "Manzana Fuji",
                        "slug": "manzana-fuji",
                        "description": "Manzana fuji, caja de 15 kg.",
                        "variants": [
                            ("Caja 15kg", 18000, 1),
                        ],
                    },
                    {
                        "name": "Tomate Ensalada",
                        "slug": "tomate-ensalada",
                        "description": "Tomate de ensalada, bandeja de 5 kg.",
                        "variants": [
                            ("Bandeja 5kg", 9000, 2),
                        ],
                    },
                ],
            },
            {
                "name": "Orgánicos",
                "slug": "organicos",
                "products": [
                    {
                        "name": "Pack Verduras Orgánicas",
                        "slug": "pack-verduras-organicas",
                        "description": "Precio variable según estación. Consulta disponibilidad.",
                        "variants": [
                            ("Caja 10kg", 25000, 1),
                        ],
                    },
                ],
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Crea tiendas, categorías, productos y variantes de prueba."

    def handle(self, *args, **options):
        for store_data in CATALOG:
            store, store_created = make_store(store_data)
            store_status = "creada" if store_created else "ya existía"
            self.stdout.write(f"[{store.slug}] Tienda {store_status}: {store.name}")

            for category_data in store_data["categories"]:
                category, _ = make_category(
                    store,
                    category_data["name"],
                    category_data["slug"],
                )
                self.stdout.write(
                    f"  └─ Categoría: {category.name} ({category.slug})"
                )

                for product_data in category_data["products"]:
                    product, _ = make_product(
                        store,
                        category,
                        product_data["name"],
                        product_data["slug"],
                        product_data["description"],
                        product_data["variants"],
                    )
                    variant_count = product.variants.count()
                    self.stdout.write(
                        f"      └─ Producto: {product.name} "
                        f"({variant_count} variantes)"
                    )

        store_count = Store.objects.count()
        category_count = Category.objects.count()
        product_count = Product.objects.count()
        variant_count = ProductVariant.objects.count()

        self.stdout.write(self.style.SUCCESS("\nResumen:"))
        self.stdout.write(self.style.SUCCESS(
            f"  Tiendas: {store_count}"
        ))
        self.stdout.write(self.style.SUCCESS(
            f"  Categorías: {category_count}"
        ))
        self.stdout.write(self.style.SUCCESS(
            f"  Productos: {product_count}"
        ))
        self.stdout.write(self.style.SUCCESS(
            f"  Variantes: {variant_count}"
        ))
