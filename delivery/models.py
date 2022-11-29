from django.db import models
from products.models import Product
from django.contrib.auth import get_user_model
from datetime import datetime
from djgeojson.fields import PointField
from django.utils import timezone

User = get_user_model()


class Pedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    ubicacion = PointField('Ingrese su ubicación: ', null=True, blank=True)
    total = models.FloatField(default=0)
    ESTADO = (
        ('p', 'Pendiente'),
        ('e', 'Entregado'),
        ('c', 'En Camino')
    )
    estado = models.CharField(max_length=1, choices=ESTADO,
    blank=True, default='p', help_text='Estado del Pedido')
    #products = models.ManyToOneRel(field="CartItem", field_name="id", to="id")


# Create your models here.
class DetallePedido(models.Model):
    amount = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="products")
    
