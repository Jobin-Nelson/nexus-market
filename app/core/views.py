from django.shortcuts import render
from rest_framework import generics

from core.models import DigitalProduct, PhysicalProduct
from core.serializers import DigitalProductSerializer, PhysicalProductSerializer

# Create your views here.


def index(request):
    context = {}
    return render(request, 'core/index.html', context)


def secret(request):
    context = {}
    return render(request, 'core/secret.html', context)


# List views
# class PhysicalProductListAPIView(generics.ListAPIView):
#     queryset = PhysicalProduct.objects.all()
#     serializer_class = PhysicalProductSerializer


class PhysicalProductListAPIView(generics.ListCreateAPIView):
    queryset = PhysicalProduct.objects.all()
    serializer_class = PhysicalProductSerializer


class DigitalProductListAPIView(generics.ListCreateAPIView):
    queryset = DigitalProduct.objects.all()
    serializer_class = DigitalProductSerializer


# Detail view
class PhysicalProductDetailsAPIView(generics.RetrieveAPIView):
    queryset = PhysicalProduct.objects.all()
    serializer_class = PhysicalProductSerializer
    lookup_url_kwarg = "physicalproduct_id"
