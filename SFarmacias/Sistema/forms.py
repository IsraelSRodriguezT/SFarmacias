from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Pedido,Venta

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cantidad', 'medicamento', 'venta', 'cliente', 'sucursal']

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['fecha', 'tipo_pago']