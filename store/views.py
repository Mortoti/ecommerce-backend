from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer
from django.db.models import Count
from rest_framework.views import APIView



# Create your views here.
class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductDetail(APIView):

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)




            







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

