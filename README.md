# Catálogo — Plataforma multitenant (Lab de práctica)

Proyecto de práctica para aprender desarrollo Django y testing de seguridad: 
una plataforma B2B de catálogos donde cada **tienda** tiene su propio catálogo
de categorías, productos y variantes, aislados por tenant.

> ⚠️ **Aviso de seguridad**
> Este repositorio es un **campo de tiro de práctica**. No es código de
> producción: no está endurecido a propósito, no garantiza ningún nivel de
> seguridad y contiene credenciales de demostración. Úsalo solo en local
> para aprender, no lo despliegues en Internet ni lo uses con datos reales.

## Características

- **Multitenant por ruta**: cada tienda vive en `/catalogo/<slug>/...`
  (antes se usaban subdominios, se reemplazaron por rutas para no depender
  de `/etc/hosts`).
- **Catálogo por tienda**: categorías → productos → variantes, con precios
  B2B y cantidad mínima de compra.
- **Datos de prueba** reproducibles con un comando.
- **SQLite** por defecto en local; PostgreSQL y AWS S3 disponibles por
  configuración (desactivados).

## Stack

- Python 3.14
- Django 6.0
- SQLite (local) / PostgreSQL (opcional)
- django-storages + boto3 (S3, opcional)
- Tailwind CSS vía CDN

## Requisitos

- WSL2 con Ubuntu (recomendado) o Linux.
- Python 3.14 y `python3-venv`.
- PostgreSQL (opcional, solo si quieres usar PostgreSQL).

## Puesta en marcha (paso a paso)

```bash
# 1. Clonar y entrar al proyecto
git clone https://github.com/chriscortes-dev/catalogo.git
cd catalogo

# 2. Crear y activar el entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

> Nota: `psycopg2` está comentado en `requirements.txt` porque solo se
> necesita para PostgreSQL. Para activarlo: `sudo apt-get install -y libpq-dev`
> y descomenta la línea.

```bash
# 4. Configurar variables de entorno
cp .env.example .env
# Edita .env y pon al menos:
#   SECRET_KEY=<genera una, ej: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())">

# 5. Migrar la base de datos (crea db.sqlite3)
python manage.py migrate

# 6. Sembrar datos de prueba (4 tiendas con catálogos)
python manage.py seed_data

# 7. (Opcional) crear superusuario para el admin
python manage.py createsuperuser

# 8. Levantar el servidor
python manage.py runserver
```

## Qué puedes probar

| URL | Descripción |
| --- | --- |
| `http://localhost:8000/` | Landing pública de la plataforma |
| `http://localhost:8000/cafe-montana/` | Tienda "Café Montaña" |
| `http://localhost:8000/cafe-montana/categoria/cafe-en-grano/` | Catálogo de la categoría |
| `http://localhost:8000/cafe-montana/categoria/cafe-en-grano/producto/cafe-arabica-reserva/` | Detalle de producto con variantes |
| `http://localhost:8000/admin/` | Admin de Django |

Credenciales del admin (solo si usaste `seed_data` y creaste el superusuario
con los datos de ejemplo de tu `.env`): las que definas tú con
`createsuperuser`.

Slugs de las tiendas sembradas: `cafe-montana`, `panaderia-la-espiga`,
`distribuidora-norte`, `mercado-verde`.

## Comandos útiles

```bash
# Correr los tests
python manage.py test

# Verificar configuración
python manage.py check

# Reiniciar los datos desde cero
rm db.sqlite3
python manage.py migrate
python manage.py seed_data
```

## Estructura del proyecto

```
catalogo/
├── apps/
│   ├── stores/          # Tiendas: modelo Store, vistas y rutas públicas
│   ├── catalog/         # Categorías, Productos y Variantes
│   └── core/            # Vista pública + comando seed_data
├── config/              # Settings, URLs, WSGI/ASGI
├── templates/           # Plantillas (base, landing, catálogo, carrito)
├── static/              # CSS y JS
├── media/               # Archivos subidos (local)
├── manage.py
└── requirements.txt
```

## Configuraciones opcionales

### PostgreSQL

En `.env`:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=catalogo
DB_USER=postgres
DB_PASSWORD=...
DB_HOST=localhost
DB_PORT=5432
```

### AWS S3 (archivos en producción)

El almacenamiento por defecto cambia automáticamente a S3 cuando
`DEBUG=False`. Requiere definir en `.env`:

```
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_STORAGE_BUCKET_NAME=...
AWS_S3_REGION_NAME=...
```

## Licencia

Uso libre para fines educativos.
