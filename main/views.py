from django.shortcuts import render
from main.models import Aliment
from main.utils.OpenApi import OpenApi

# Create your views here.
def index(request):
    if len(Aliment.objects.all()) < 10*20:
        OpenApi().fill_database()
    return render(request, 'index.html',)


def mentions(request):
    return render(request, 'mentions.html')
