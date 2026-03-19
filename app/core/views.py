from django.shortcuts import render
from rest_framework import viewsets

from core.models import DigitalProduct, PhysicalProduct
from core.permissions import IsVendorOrReadOnly
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
    permission_classes = [IsVendorOrReadOnly]


class DigitalProductViewSet(viewsets.ModelViewSet):
    queryset = DigitalProduct.objects.all()
    serializer_class = DigitalProductSerializer
    permission_classes = [IsVendorOrReadOnly]
