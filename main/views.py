from django.shortcuts import render, HttpResponse, redirect
from main.models import Aliment
from main.utils.OpenApi import OpenApi
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.
def index(request):
    if len(Aliment.objects.all()) < 10*20:
        OpenApi().fill_database()
    return render(request, 'index.html',)


def mentions(request):
    return render(request, 'mentions.html')

@csrf_exempt
def search_substitutes(request):
    response = HttpResponse()
    aliment = request.POST["aliment_search"]
    aliment = Aliment.objects.filter(product_name__contains=aliment)
    substitutes = []
    if aliment:
        aliment = aliment[0]
    for i in range(0, 5):
        # get ascii value of A and add the current index to it so we can get the next letters
        nutrition_grade = chr(ord("a") + i)
        print(nutrition_grade)
        temp_substitutes = Aliment.objects.filter(category=aliment.category, nutrition_grades=nutrition_grade)
        print(temp_substitutes)
        if temp_substitutes:
            for substitute in temp_substitutes:
                substitutes.append(substitute)
        if ord(nutrition_grade) >= ord(aliment.nutrition_grades):  # if the nutrigrade is the same as the aliment's, break
            print("same as aliment")
            break
    context = {
        'aliment': aliment,
        'substitutes': substitutes,
    }
    print(aliment)
    print(substitutes)
    return render(request, 'aliments.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('register')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})