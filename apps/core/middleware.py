from urllib import request

from apps.stores.models import Store


class StoreMiddleware:
    """
    Resuelve la tienda usando subdominio.

    Ejemplo:
    tienda1.catalogo.cl → slug=tienda1
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        host = request.get_host().split(":")[0].lower().strip()

        parts = host.split(".")

        request.store = None

        # dominio base catalogo.cl
        if len(parts) >= 3:
            subdomain = parts[0]

            request.store = Store.objects.filter(
                slug=subdomain,
                is_active=True
            ).first()

        response = self.get_response(request)

        print("STORE:", request.store)
        print("HOST:", request.get_host())

        return response