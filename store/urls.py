from django.urls import path
from . import views

from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('product', views.ProductViewSet)
router.register('collection', views.CollectionViewSet)

product_routers =routers.NestedDefaultRouter(router, 'product', lookup='product')
product_routers.register('reviews', views.ReviewViewSet, basename='product-review')

# URLConf
urlpatterns = router.urls + product_routers.urls