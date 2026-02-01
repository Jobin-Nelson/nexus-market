from django.shortcuts import HttpResponse, render

# Create your views here.


def index(request):
    context = {}
    return render(request, 'core/index.html', context)


def secret(request):
    context = {}
    return render(request, 'core/secret.html', context)
