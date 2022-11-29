from django.urls import path
from delivery import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mis-pedidos/', views.PedidoListView.as_view(), name="mis_pedidos"),
    path('pedidos/', views.PedidoAdminListView.as_view(), name='pedidos'),
    path('map/<int:idPedido>', views.mapaPedido, name='map_pedido'),
]
    
