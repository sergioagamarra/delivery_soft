from django.urls import path

#from .views import posts,home,post,create_post,edit_post, delete_post

from . import views
app_name = 'products'
urlpatterns = [
    path('', views.products, name='products'),
    path('search', views.search_product, name='product_search'),
    path('category/<int:idCategory>', views.filter_by_category, name='product_filter_category'),
    path('add', views.add_product, name='add_product'),
    path('edit/<int:idProduct>', views.edit_product, name='edit_product'),
    #ath('price/<int:asc>', views.filter_by_price, name='product_filter_price')
]