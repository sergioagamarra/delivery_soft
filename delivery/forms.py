from django import forms
from .models import Pedido
from django.forms.widgets import NumberInput
from leaflet.forms.widgets import LeafletWidget
from django.contrib.gis.db import models as geo_models


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ('ubicacion',)
        widgets = {
            #'fecha': NumberInput(attrs={'type': 'date'}),
            'ubicacion': LeafletWidget({
                'map_height': '500px',
                'map_width': '100%',
                'map_srid': 4326,
            })
        }