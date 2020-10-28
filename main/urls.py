from django.urls import path, include
import main.views as main
from django.contrib.auth import views as auth_views

app_name = "main"

urlpatterns = [
    path('', main.index, name="index"),
    path('mentions/', main.mentions, name="mentions"),
    path('register/', main.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/password_change.html',
            success_url='/',
        ),
        name='password_change'
    ),
    path('search_substitute/', main.search_substitutes, name='search_substitutes'),
    path('saved_substitutes/', main.show_saved_substitutes, name='show_saved_substitutes'),
    path('aliment_info/<int:aliment_id>/', main.show_aliment_info, name='show_aliment_info'),
    path('save_substitute/<int:substitute_id>/', main.save_substitute, name='save_substitute'),
    path('delete_substitute/<int:substitute_id>/', main.delete_substitute, name='delete_substitute'),
]