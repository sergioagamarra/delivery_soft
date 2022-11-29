from django.shortcuts import render
from .models import Product
from .models import Category
from django.views import generic 
from django.core.paginator import Paginator
from django.db import IntegrityError

# Create your views here.
def products(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    page_number = request.GET.get('page')
    paginator = Paginator(products, 5)
    page_obj = paginator.get_page(page_number)
    return render(request, "products.html",{
        #"products": products,
        "categories": categories,
        "page_obj": page_obj
    })

def add_product(request):
    categories = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        image = request.POST['image']
        id_category = request.POST['category']
        if id_category == "Abrir este menú de selección":
            return render(request, "product.html", {
                "errorCategory": True,
                "categories": categories
            })
        try:
            new_product = Product()
            new_product.name = name
            new_product.price = price
            new_product.description = description
            new_product.image = image
            category = Category.objects.filter(id=id_category).first()
            new_product.category = category
            new_product.save()
            return render(request, "product.html", {
                "productAdd": True,
                "categories": categories
            })
        except IntegrityError:
            return render(request, "product.html", {
                "errorAdd": True,
                "categories": categories
            })
    return render(request, "product.html",{
        "categories": categories
    })

def edit_product(request, idProduct):
    product = Product.objects.filter(id=idProduct).first()
    categories = Category.objects.all()
    if request.method == "POST":
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.description = request.POST['description']
        product.image = request.POST['image']
        category = Category.objects.filter(id=request.POST['category']).first()
        product.category = category
        product.save()
        return render(request, "product.html", {
            "edit": True,
            "product": product,
            "productEdit": True,
            "categories": categories
        })
    return render(request, "product.html", {
        "edit": True,
        "product": product,
        "categories": categories
    })


def search_product(request):
    if request.method == "POST":
        search = request.POST['search']
        products = Product.objects.filter(name__icontains = search)
        categories = Category.objects.all()
    
        return render(request, "products.html",{
            "page_obj": products,
            "categories": categories
        })
    
def filter_by_category(request, idCategory):
    products = Product.objects.filter(category=idCategory)
    categories = Category.objects.all()
    page_number = request.GET.get('page')
    paginator = Paginator(products, 5)
    page_obj = paginator.get_page(page_number)
    return render(request, "products.html",{
        "page_obj": page_obj,
        "categories": categories
    })
    
""" def filter_by_price(request, asc):
    if asc == 1:
        products = Product.objects.all().order_by("price")
    else: 
        products = Product.objects.all().order_by("-price")
    categories = Category.objects.all()
    return render(request, "pages/home.html",{
        "products": products,
        "categories": categories
    }) """