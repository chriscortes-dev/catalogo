from django.urls import path
from . import views

urlpatterns = [

    path("", views.store_landing_view, name="store_landing"),

    path(
        "categoria/<slug:category_slug>/",
        views.catalog_view,
        name="catalog"
    ),

    path(
        "categoria/<slug:category_slug>/producto/<slug:product_slug>/",
        views.product_detail_view,
        name="product_detail"
    )

]