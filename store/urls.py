from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('product', views.ProductViewSet)
router.register('collection', views.CollectionViewSet)

# URLConf
urlpatterns = router.urls