from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import  ListCreateAPIView



# Create your views here.
class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    def get_serializer_context(self):
        return  {'request': self.request}

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




            







class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(product_count=Count('products'))
    serializer_class = CollectionSerializer


@api_view()
def collection_detail(request, pk):
    collection = get_object_or_404(Collection.objects.annotate(product_count = Count('products')), pk=pk)
    serializer = CollectionSerializer(collection)

    return Response(serializer.data)

