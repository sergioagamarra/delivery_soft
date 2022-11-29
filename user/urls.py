from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("perfil/<int:idUser>", login_required(views.perfil_view), name="perfil"),
    path("edit/<int:idUser>", views.edit_user, name="edit_user"),
    path("clients/", views.clients, name="clients"),
    path('search', views.search_client, name='client_search'),
]