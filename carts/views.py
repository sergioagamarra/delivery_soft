from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import CartItem, Cart
from .models import Product
from products.models import Product
from delivery.models import Pedido, DetallePedido
from django.utils.decorators import decorator_from_middleware
from user.middleware import AuthMiddleware
from django.views.decorators.csrf import csrf_exempt
from delivery.forms import PedidoForm
import json


paypal_url = "https://api-m.sandbox.paypal.com"
paypal_client_id = "Afe9hlW9w8UAJlATaxKkjmxMT4z1MfHjwviMKPC-rqmfVlyOEhUYuwwO4azjTVjbBoxW7lXRX194snWc"
paypal_client_secret = "EPv-kS_PxCK-5_tJtKORQjTbNRI2hVkR3aKtCNE5xmcekbvYhF_EHA1Fzj1C2C8S5Bn_Yd0K1up4iphj"

# Create your views here.
auth_middleware = decorator_from_middleware(AuthMiddleware)


@auth_middleware
def get_cart(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            formulario = PedidoForm(request.POST)
            if formulario.is_valid():
                pedido = formulario.save(commit=False)
                pedido.user = request.user
                if formulario.cleaned_data['ubicacion'] is None:
                    products = request.user.cart.products.all()
                    total = request.user.cart.total
                    formulario = PedidoForm()
                    # for cartItem in products:
                    #     total += cartItem.product.price * cartItem.amount
                    return render(request, "cart.html", {
                        "products": products,
                        "total": total,
                        "formulario": formulario,
                        "error": True
                    })
                products = request.user.cart.products.all()
                pedido.ubicacion = formulario.cleaned_data['ubicacion']
                pedido.total = request.user.cart.total
                pedido.save()
                for d in products:
                    detalle = DetallePedido()
                    detalle.amount = d.amount
                    detalle.product = d.product
                    detalle.pedido = pedido
                    detalle.save()
                cart_items = request.user.cart.delete()
                new_cart = Cart()
                new_cart.user = request.user
                new_cart.save()
                return redirect('/products')
                
        products = request.user.cart.products.all()
        total = request.user.cart.total
        formulario = PedidoForm()
        # for cartItem in products:
        #     total += cartItem.product.price * cartItem.amount
        return render(request, "cart.html", {
            "products": products,
            "total": total,
            'formulario': formulario
        })

    return render(request, "login.html", {
            "message": "Email validated successfully",
            "validate": False
        })


def add_to_cart(request, idProduct):
    if request.user.is_authenticated:
        
        products = request.user.cart.products.all()
        if products.first() is None:
            newCartItem = CartItem()
            newCartItem.product = Product.objects.get(pk=idProduct)
            newCartItem.amount = 1
            newCartItem.cart = request.user.cart
            newCartItem.save()
        else: 
            exist = False
            for cartItem in products:        
                if cartItem.product.id == idProduct:
                    exist = True
                    aux = cartItem
            if exist:   
                aux.amount += 1
                aux.save()
            else:
                newCartItem = CartItem()
                newCartItem.product = Product.objects.get(pk=idProduct)
                newCartItem.amount = 1
                newCartItem.cart = request.user.cart
                newCartItem.save()


        #actualizar el total
        products = request.user.cart.products.all()
        total = 0
        for cartItem in products:
            total += cartItem.product.price * cartItem.amount
        cart = request.user.cart
        cart.total=total
        cart.save()
        return redirect("/products")

    return render(request, "login.html", {
                        "errorInicio": True
                    })


@csrf_exempt
def change_amount(request):
    if request.method == "POST":
        data = json.loads(request.body)

        amount = data['amount']
        id_item = data['idItem']

        cart_item = CartItem.objects.get(id=id_item)

        cart_item.amount = amount
        cart_item.save()

        #actualizar el total
        products = request.user.cart.products.all()
        total = 0
        for cartItem in products:
            total += cartItem.product.price * cartItem.amount

        cart = request.user.cart
        cart.total=total
        cart.save()
        print(cart.total)

        return JsonResponse({
            "total": total
        })

def delete_from_cart(request, id_cart_item):
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(pk=id_cart_item)
        if cart_item.cart.user == request.user:
            cart_item.delete()
            total = calculate_total(request.user.cart)
            return redirect("/cart")

    return redirect("/")


def calculate_total(cart):
    products = cart.products.all()
    total = 0
    for cartItem in products:
        total += cartItem.product.price * cartItem.amount

    updateCart = cart
    updateCart.total = total
    updateCart.save()
    return total

