from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from carts.models import Cart
from django.core.paginator import Paginator
import uuid

User = get_user_model()


# Create your views here.
def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                if user.is_admin:
                    return redirect("/pedidos")
                else:
                    return redirect("/")
            else:
                return render(request, "login.html", {
                    "error": "Inactive account"
                })
        return render(request, "login.html", {
            "errorCredenciales": "Invalid credentials"
        })

    if request.user.is_authenticated:
        if request.user.id_admin:
            return redirect("/pedidos")
        return redirect("/")
    return render(request, "login.html")


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect("/auth/login")


def signup_view(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']
        email = request.POST['email']
        barrio = request.POST['barrio']
        calle = request.POST['calle']
        numero = request.POST['numero']

        if password_confirmation != password:
            return render(request, "signup.html", {
                "errorPassword": True
            })

        try:

            new_user = User.objects.create_user(username, email, password)
            cart = Cart()
            cart.user = new_user
            cart.save()
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.barrio = barrio
            new_user.calle = calle
            new_user.numero = numero
            new_user.save()

            login(request, new_user)
            return redirect("/")

        except IntegrityError:
            return render(request, "signup.html", {
                "errorEmailReg": True
            })

    return render(request, "signup.html")

def perfil_view(request, idUser):
    client = User.objects.filter(id=idUser).first()
    
    return render(request, "perfil.html", {
        "client": client
    })

def edit_user(request, idUser):
    client = User.objects.filter(id=idUser).first()
    if request.method == "POST":
        client.first_name = request.POST['first_name']
        client.last_name = request.POST['last_name']
        client.username = request.POST['username']
        client.email = request.POST['email']
        client.barrio = request.POST['barrio']
        client.calle = request.POST['calle']
        client.numero = request.POST['numero']

        client.save()

        return render(request, "perfil.html", {
            "client": client,
            "messageEdit": True
        })
        
    return render(request, "perfil.html", {
        "client": client,
    })

def clients(request):
    if request.user.is_authenticated:
        clients = User.objects.all()
        page_number = request.GET.get('page')
        paginator = Paginator(clients, 10)
        page_obj = paginator.get_page(page_number)
        return render(request, "clients.html",{
            "page_obj": page_obj
        })
    return redirect("/products")

def search_client(request):
    if request.method == "POST":
        search = request.POST['search']
        if search == "":
            return redirect("/auth/clients")
        clients = User.objects.filter(email__icontains = search)
        return render(request, "clients.html",{
            "page_obj": clients
        })

""" def validate_email(request, email_uuid):
    try:
        user = User.objects.get(emailValidationUUID=email_uuid)
        user.emailValidationUUID = None
        user.isEmailValid = True
        user.save()

        return render(request, "pages/email_validation.html", {
            "message": "Email validated successfully",
            "type": True,
            "validate": True
        })

    except ObjectDoesNotExist:
        return render(request, "pages/email_validation.html", {
            "message": "Maybe this validation code has been used. Verify your url",
            "type": False,
            "validate": True
        }) """