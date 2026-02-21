from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('secret/', views.secret, name='secret'),
    path('physical_products/', views.PhysicalProductListAPIView.as_view(), name='physical_product'),
    path('digital_products/', views.DigitalProductListAPIView.as_view(), name='digital_product'),
    path('physical_products/<int:pk>', views.PhysicalProductDetailsAPIView.as_view(), name='physical_product_details'),
]
