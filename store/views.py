from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer
from django.db.models import Count



# Create your views here.

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status= status.HTTP_201_CREATED)

            



@api_view(['GET', 'PUT'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return  Response(serializer.data)
@api_view()
def collection_list(request):
    queryset = Collection.objects.annotate(product_count = Count('products'))
    serializer = CollectionSerializer(queryset, many = True)
    return Response(serializer.data)
@api_view()
def collection_detail(request, pk):
    collection = get_object_or_404(Collection.objects.annotate(product_count = Count('products')), pk=pk)
    serializer = CollectionSerializer(collection)

    return Response(serializer.data)

