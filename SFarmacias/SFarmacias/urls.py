"""
URL configuration for SFarmacias project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Sistema import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('login/', views.login, name='login'),
    path('productos/', views.productos, name='productos'),
    path('sucursales/', views.sucursales, name='sucursales'),
    path('user/', views.user, name='user'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('crear_pedido/', views.crear_pedido, name='crear_pedido'),
    path('actualizar_pedido/<int:pedido_id>/', views.actualizar_pedido, name='actualizar_pedido'),
    path('lista_pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('verificar_inventario/<int:pedido_id>/', views.verificar_inventario_view, name='verificar_inventario'),
    path('crear_venta/', views.crear_venta, name='crear_venta'),
    path('actualizar_venta/<int:venta_id>/', views.actualizar_venta, name='actualizar_venta'),
    path('lista_ventas/', views.lista_ventas, name='lista_ventas'),
    path('verificar_inventario/<int:pedido_id>/', views.verificar_inventario_view, name='verificar_inventario'),
]
