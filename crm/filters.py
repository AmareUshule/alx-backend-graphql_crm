import django_filters
from django_filters import FilterSet, CharFilter, DateFilter, NumberFilter
from .models import Customer, Product, Order
import re

class CustomerFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    email = CharFilter(field_name='email', lookup_expr='icontains')
    created_at_gte = DateFilter(field_name='created_at', lookup_expr='gte')
    created_at_lte = DateFilter(field_name='created_at', lookup_expr='lte')
    
    # Custom filter for phone number pattern
    phone_pattern = CharFilter(method='filter_phone_pattern')
    
    def filter_phone_pattern(self, queryset, name, value):
        # Filter phones starting with a specific pattern
        return queryset.filter(phone__startswith=value)
    
    class Meta:
        model = Customer
        fields = ['name', 'email']

class ProductFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    price_gte = NumberFilter(field_name='price', lookup_expr='gte')
    price_lte = NumberFilter(field_name='price', lookup_expr='lte')
    stock_gte = NumberFilter(field_name='stock', lookup_expr='gte')
    stock_lte = NumberFilter(field_name='stock', lookup_expr='lte')
    
    # Custom filter for low stock
    low_stock = NumberFilter(method='filter_low_stock')
    
    def filter_low_stock(self, queryset, name, value):
        # Filter products with stock less than specified value
        return queryset.filter(stock__lt=value)
    
    class Meta:
        model = Product
        fields = ['name', 'price', 'stock']

class OrderFilter(FilterSet):
    total_amount_gte = NumberFilter(field_name='total_amount', lookup_expr='gte')
    total_amount_lte = NumberFilter(field_name='total_amount', lookup_expr='lte')
    order_date_gte = DateFilter(field_name='order_date', lookup_expr='gte')
    order_date_lte = DateFilter(field_name='order_date', lookup_expr='lte')
    
    # Filter by related customer name
    customer_name = CharFilter(field_name='customer__name', lookup_expr='icontains')
    
    # Filter by related product name (through many-to-many)
    product_name = CharFilter(method='filter_product_name')
    
    # Filter by specific product ID
    product_id = NumberFilter(method='filter_product_id')
    
    def filter_product_name(self, queryset, name, value):
        # Filter orders that have products with names containing the value
        return queryset.filter(products__name__icontains=value).distinct()
    
    def filter_product_id(self, queryset, name, value):
        # Filter orders that contain a specific product
        return queryset.filter(products__id=value).distinct()
    
    class Meta:
        model = Order
        fields = ['total_amount', 'order_date']