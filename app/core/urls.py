from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    r'physicalproducts', views.PhysicalProductViewSet, basename='phsyicalproduct'
)
router.register(
    r'digitalproducts', views.DigitalProductViewSet, basename='digitalproduct'
)

urlpatterns = [
    path('', views.index, name='index'),
    path('secret/', views.secret, name='secret'),
    path('api/', include(router.urls)),
]
