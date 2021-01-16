from django.shortcuts import render, redirect
from main.models import Aliment, Substitute
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator

def index(request):
    return render(request, 'index.html',)


def mentions(request):
    return render(request, 'mentions.html')


def search_substitutes(request):
    """
    This view gets an aliment name in a post request and renders a list of its substitutes if it finds some,
    redirects to the index if its not a post request
    """
    if request.method == "GET":
        aliment_search = request.GET["aliment_search"]  # The text searched by the user
        try:
            page = request.GET["page"]
        except:
            page = 1
        aliment = Aliment.objects.filter(product_name__contains=aliment_search)
        substitutes = []
        if aliment:
            aliment = aliment[0]  # If we found at least 1 aliment, put it in the aliment variable
            for i in range(0, 5):
                # get ascii value of A and add the current index to it so we can get the next letters
                nutrition_grade = chr(ord("a") + i)
                # Get the substitutes of the same category and the nutrition grade we're at in the loop
                temp_substitutes = Aliment.objects.filter(category=aliment.category, nutrition_grades=nutrition_grade)
                if temp_substitutes:
                    for substitute in temp_substitutes:
                        substitutes.append(substitute)
                # if the nutrigrade is the same as the aliment's, break
                try:
                    if ord(nutrition_grade) >= ord(aliment.nutrition_grades):
                        break
                except:
                    pass
            if substitutes:
                pages = Paginator(substitutes, 6)
                page_object = pages.get_page(page)
            else:
                page_object = None
            context = {
                'aliment': aliment,
                'aliment_search': aliment_search,
                'substitutes': substitutes,
                'page_object': page_object,
            }
        else:
            context = {
                'aliment': False,
            }
        return render(request, 'aliments.html', context)
    else:
        return redirect("main:index")


def show_aliment_info(request, aliment_id):
    """
    Gets an aliment and renders a page containing its infos

    :param aliment_id: The id of the clicked aliment
    :type aliment_id: int
    """
    context = {}
    if request.method == 'GET':
        context["aliment"] = Aliment.objects.get(id=aliment_id)
        return render(request, "aliment_info.html", context)


def show_saved_substitutes(request):
    """
    Gets the user's saved substitutes and renders a list of them
    """
    context = {}
    if request.user.is_authenticated:
        page = request.GET.get("page", 1)
        context["substitutes"] = Substitute.objects.filter(user=request.user)
        if context["substitutes"]:
            pages = Paginator(context["substitutes"], 6)
            page_object = pages.get_page(page)
        else:
            page_object = None
        context["page_object"] = page_object
        return render(request, 'saved_substitutes.html', context)


def save_substitute(request, substitute_id):
    """
    Saves a substitute in the database.

    :param substitute_id: The id of the aliment we have to save as a substitute
    :type substitute_id: int
    """
    context = {}
    if request.method == 'GET' and request.user.is_authenticated:
        aliment = Aliment.objects.get(id=substitute_id)
        try:
            substitute_data = dict(vars(aliment))  # Get the aliments info as a dict
            try:
                # remove the unnecessary values so we can unpack it into substitutes
                substitute_data.pop('id')
                substitute_data.pop('_state')
            except KeyError:
                pass
            # add some necessary data that aren't in the aliments infos
            substitute_data['aliment'] = aliment
            substitute_data["user"] = request.user
            Substitute.objects.create(**substitute_data)
            context["save_successful"] = True
        except Exception as e:
            context["save_successful"] = False
    return render(request, 'substitute_response.html', context)


def delete_substitute(request, substitute_id):
    """
    Deletes a saved substitute

    :param substitute_id: The id of the substitute we have to delete
    :type substitute_id: int
    """
    if request.user.is_authenticated:
        Substitute.objects.get(id=substitute_id).delete()
        return redirect('main:show_saved_substitutes')


def register(request):
    """
    Registers a user with the data we got in the registration form
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('main:login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
