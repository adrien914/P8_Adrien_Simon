from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html',)


def mentions(request):
    return render(request, 'mentions.html')
