from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic 
from delivery.models import Pedido, DetallePedido
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

""" def pedidos(request):
    return render(request, 'pedidos.html', {}) """

def mapaPedido(request, idPedido):
    pedido = Pedido.objects.filter(id=idPedido).first()
    return render(request, 'map.html', {
        "pedido": pedido
    })

class PedidoAdminListView(generic.ListView):
    model = Pedido
    context_object_name = 'pedidos'
    # en este caso va un modelo
    #queryset = get_queryset()
    
    # si quiero filtrar
    template_name='pedidos.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {
            "pedidos": list()
        }

        pedidos = Pedido.objects.filter(estado='p').order_by('-fecha')
        pedido = {}
        for p in pedidos:
            pedido = {
                "id": p.id,
                "fecha": p.fecha.strftime('%d-%m-%Y'),
                "ubicacion": p.ubicacion,
                "total": int(p.total),
                "estado": p.estado,
                "detalles": list()
            }
            detalles = DetallePedido.objects.filter(pedido = p)
            for d in detalles:
                d.product.price = int(d.product.price)
                pedido["detalles"].append(d)
            context["pedidos"].append(pedido)
            page_number = self.request.GET.get('page')
            paginator = Paginator(context["pedidos"], 4)
            page_obj = paginator.get_page(page_number)
            context["page_obj"] = page_obj
        return context


class PedidoListView(generic.ListView):
    model = Pedido
    context_object_name = 'pedidos'
    # en este caso va un modelo
    #queryset = get_queryset()
    
    # si quiero filtrar
    template_name='mis_pedidos.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {
            "pedidos": list()
        }

        pedidos = Pedido.objects.filter(user=self.request.user).order_by('-fecha')
        pedido = {}
        for p in pedidos:
            pedido = {
                "id": p.id,
                "fecha": p.fecha.strftime('%d-%m-%Y'),
                "ubicacion": p.ubicacion,
                "total": int(p.total),
                "estado": p.estado,
                "detalles": list()
            }
            detalles = DetallePedido.objects.filter(pedido = p)
            for d in detalles:
                d.product.price = int(d.product.price)
                pedido["detalles"].append(d)
            context["pedidos"].append(pedido)
            page_number = self.request.GET.get('page')
            paginator = Paginator(context["pedidos"], 4)
            page_obj = paginator.get_page(page_number)
            context["page_obj"] = page_obj
        return context
 # nombre del template """

