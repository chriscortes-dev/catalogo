from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Prefetch

from apps.catalog.models import Category, Product, ProductVariant
from apps.stores.models import Store


def _get_store(store_slug):
    return get_object_or_404(
        Store,
        slug=store_slug,
        is_active=True
    )


def store_landing_view(request, store_slug):

    store = _get_store(store_slug)

    categories = Category.objects.filter(
        store=store,
        is_active=True
    )

    return render(request, "stores/landing.html", {
        "store": store,
        "categories": categories
    })


def catalog_view(request, store_slug, category_slug):

    store = _get_store(store_slug)

    category = get_object_or_404(
        Category,
        store=store,
        slug=category_slug,
        is_active=True
    )

    products_qs = (
        Product.objects
        .filter(
            store=store,
            category=category,
            is_active=True
        )
        .prefetch_related(
            Prefetch(
                "variants",
                queryset=ProductVariant.objects.filter(is_active=True)
            )
        )
    )

    paginator = Paginator(products_qs, 20)  # 20 productos por página
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)

    return render(request, "catalog/catalog.html", {
        "store": store,
        "category": category,
        "products": products
    })


def product_detail_view(request, store_slug, category_slug, product_slug):

    store = _get_store(store_slug)

    category = get_object_or_404(
        Category,
        store=store,
        slug=category_slug,
        is_active=True
    )

    product = get_object_or_404(
        Product.objects.prefetch_related(
            Prefetch(
                "variants",
                queryset=ProductVariant.objects.filter(is_active=True)
            )
        ),
        store=store,
        category=category,
        slug=product_slug,
        is_active=True
    )

    return render(request, "catalog/product_detail.html", {
        "store": store,
        "product": product,
        "category_slug": category_slug,
        "product_slug": product_slug,
        "variants": product.variants.all()
    })