from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Product, Collection, Review
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import  ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet



# Create your views here.
class ProductViewSet(ModelViewSet):

    serializer_class = ProductSerializer
    def get_queryset(self):
        queryset = Product.objects.all()
        collection_id = self.request.query_params.get('collection_id')
        if collection_id is not None:
            queryset = queryset.filter(collection_id= collection_id)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return  Response ({'error': "The product you're trying to delete has associated orders"})
        product.delete()
        return Response (status=status.HTTP_204_NO_CONTENT)



class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(product_count=Count('products'))
    serializer_class = CollectionSerializer

class ReviewViewSet(ModelViewSet):

    serializer_class = ReviewSerializer
    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_pk'])
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}







