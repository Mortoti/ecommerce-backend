from rest_framework import serializers
from decimal import Decimal
from .models import Product, Collection, Review



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug',  'inventory', 'description',
                  'unit_price','collection', 'price_with_tax' ]
    price_with_tax = serializers.SerializerMethodField(method_name= 'calculate_tax')



    def calculate_tax(self, product):
        return product.unit_price * Decimal(1.1)
class CollectionSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField()
    class Meta:
        model = Collection
        fields = ['id', 'title', 'product_count']
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'date', 'description', 'product']
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id= product_id, **validated_data)


