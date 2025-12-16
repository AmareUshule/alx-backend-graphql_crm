import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graphql_crm.settings")
django.setup()

from crm.models import Customer, Product

Customer.objects.get_or_create(
    name="Seed User",
    email="seed@example.com"
)

Product.objects.get_or_create(
    name="Seed Product",
    price=100.00,
    stock=5
)

print("Database seeded successfully")
