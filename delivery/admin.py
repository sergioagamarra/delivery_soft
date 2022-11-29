from django.contrib import admin
from .models import Pedido
from .models import DetallePedido
from leaflet.admin import LeafletGeoAdmin

# Register your models here.
admin.site.register(Pedido, LeafletGeoAdmin)
admin.site.register(DetallePedido)