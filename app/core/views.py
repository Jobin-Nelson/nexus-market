from django.shortcuts import render
from rest_framework import generics, viewsets

from core.models import DigitalProduct, PhysicalProduct
from core.serializers import DigitalProductSerializer, PhysicalProductSerializer

# Create your views here.


def index(request):
    context = {}
    return render(request, 'core/index.html', context)


def secret(request):
    context = {}
    return render(request, 'core/secret.html', context)


# API
class PhysicalProductViewSet(viewsets.ModelViewSet):
    queryset = PhysicalProduct.objects.all()
    serializer_class = PhysicalProductSerializer

class DigitalProductViewSet(viewsets.ModelViewSet):
    queryset = DigitalProduct.objects.all()
    serializer_class = DigitalProductSerializer
