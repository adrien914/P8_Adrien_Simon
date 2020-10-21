"""nutella URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import main.views as main
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', main.index),
    path('mentions/', main.mentions),
    path('register/', main.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/password_change.html',
            success_url = '/'
        ),
        name='password_change'
    ),
    path('aliment_info/<int:aliment_id>/', main.show_aliment_info),
    path('search_substitute/', main.search_substitutes),
    path('saved_substitutes/', main.show_saved_substitutes),
    path('save_substitute/<int:substitute_id>/', main.save_substitute),
    path('delete_substitute/<int:substitute_id>/', main.delete_substitute),
    path('admin/', admin.site.urls),
]
