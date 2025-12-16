import re
import graphene
from django.db import transaction
from graphene_django import DjangoObjectType, DjangoFilterConnectionField
from graphene import relay
from .models import Customer, Product, Order
from .filters import CustomerFilter, ProductFilter, OrderFilter
from django.utils import timezone

# GraphQL Types with Node support
class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        interfaces = (relay.Node,)
        fields = "__all__"
        filter_fields = {}

class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        interfaces = (relay.Node,)
        fields = "__all__"
        filter_fields = {}

class OrderNode(DjangoObjectType):
    class Meta:
        model = Order
        interfaces = (relay.Node,)
        fields = "__all__"
        filter_fields = {}

# Define Input Object Type for bulk creation
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

# Mutations

# CreateCustomer
class CreateCustomer(graphene.Mutation):
    customer = graphene.Field(CustomerNode)
    message = graphene.String()

    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    def mutate(self, info, name, email, phone=None):
        if Customer.objects.filter(email=email).exists():
            raise Exception("Email already exists")

        if phone and not re.match(r"^(\+\d{10,15}|\d{3}-\d{3}-\d{4})$", phone):
            raise Exception("Invalid phone format")

        customer = Customer.objects.create(
            name=name,
            email=email,
            phone=phone
        )

        return CreateCustomer(
            customer=customer,
            message="Customer created successfully"
        )

# BulkCreateCustomers (Partial Success)
class BulkCreateCustomers(graphene.Mutation):
    customers = graphene.List(CustomerNode)
    errors = graphene.List(graphene.String)

    class Arguments:
        input = graphene.List(graphene.NonNull(CustomerInput), required=True)

    def mutate(self, info, input):
        created = []
        errors = []

        with transaction.atomic():
            for idx, data in enumerate(input):
                if Customer.objects.filter(email=data.email).exists():
                    errors.append(f"Row {idx + 1}: Email already exists")
                    continue

                customer = Customer.objects.create(
                    name=data.name,
                    email=data.email,
                    phone=data.phone
                )
                created.append(customer)

        return BulkCreateCustomers(customers=created, errors=errors)

# CreateProduct
class CreateProduct(graphene.Mutation):
    product = graphene.Field(ProductNode)

    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        stock = graphene.Int()

    def mutate(self, info, name, price, stock=0):
        if price <= 0:
            raise Exception("Price must be positive")
        if stock < 0:
            raise Exception("Stock cannot be negative")

        product = Product.objects.create(
            name=name,
            price=price,
            stock=stock
        )

        return CreateProduct(product=product)

# CreateOrder
class CreateOrder(graphene.Mutation):
    order = graphene.Field(OrderNode)

    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)
        order_date = graphene.DateTime()

    def mutate(self, info, customer_id, product_ids, order_date=None):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            raise Exception("Invalid customer ID")

        if not product_ids:
            raise Exception("At least one product must be selected")

        products = Product.objects.filter(id__in=product_ids)
        if products.count() != len(product_ids):
            raise Exception("Invalid product ID")

        total = sum([p.price for p in products])

        order = Order.objects.create(
            customer=customer,
            total_amount=total,
            order_date=order_date or timezone.now()
        )

        order.products.set(products)
        return CreateOrder(order=order)

# Query & Mutation Containers with Filtering
class Query(graphene.ObjectType):
    # Filtered connections
    all_customers = DjangoFilterConnectionField(
        CustomerNode,
        filterset_class=CustomerFilter
    )
    
    all_products = DjangoFilterConnectionField(
        ProductNode,
        filterset_class=ProductFilter
    )
    
    all_orders = DjangoFilterConnectionField(
        OrderNode,
        filterset_class=OrderFilter
    )
    
    # Legacy queries (kept for backward compatibility)
    customers = graphene.List(CustomerNode)
    products = graphene.List(ProductNode)
    orders = graphene.List(OrderNode)

    def resolve_customers(self, info):
        return Customer.objects.all()

    def resolve_products(self, info):
        return Product.objects.all()

    def resolve_orders(self, info):
        return Order.objects.all()


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()