from django.shortcuts import render, redirect
from main.models import Aliment, Substitute
from main.utils.OpenApi import OpenApi
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import traceback

# Create your views here.
def index(request):
    if len(Aliment.objects.all()) < 10*20:
        OpenApi().fill_database()
    return render(request, 'index.html',)


def mentions(request):
    return render(request, 'mentions.html')

def search_substitutes(request):
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
                break
        context = {
            'aliment': aliment,
            'substitutes': substitutes[:9],
        }
    else:
        context = {
            'aliment': False,
        }
    return render(request, 'aliments.html', context)

def show_aliment_info(request, aliment_id):
    context = {}
    if request.method == 'GET':
        context["aliment"] = Aliment.objects.get(id=aliment_id)
        return render(request, "aliment_info.html", context)

def show_saved_substitutes(request):
    context = {}
    if request.user.is_authenticated:
        context["substitutes"] = Substitute.objects.filter(user=request.user)
        return render(request, 'saved_substitutes.html', context)

def save_substitute(request, substitute_id):
    context = {}
    if request.method == 'GET' and request.user.is_authenticated:
        aliment = Aliment.objects.get(id=substitute_id)
        try:
            substitute_data = dict(vars(aliment))
            try:
                substitute_data.pop('id')
                substitute_data.pop('_state')
            except KeyError:
                pass
            substitute_data['aliment'] = aliment
            substitute_data["user"] = request.user
            Substitute.objects.create(**substitute_data)
            context["save_successful"] = True
        except Exception as e:
            context["save_successful"] = False
    return render(request, 'substitute_response.html', context)


def delete_substitute(request, substitute_id):
    if request.user.is_authenticated:
        Substitute.objects.get(id=substitute_id).delete()
        return redirect(show_saved_substitutes)


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
