from django.shortcuts import render, get_object_or_404, redirect
from .models import Pedido, Medicamento, Venta, Sucursal
from django.contrib.auth import login as auth_login, authenticate
from .forms import CustomLoginForm,PedidoForm,VentaForm
from django.contrib import messages

def home(request):
    return render(request,'home.html')

def login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Inicio de sesión exitoso')
                if user.groups.filter(name='Clientes').exists():
                    return redirect('user')
                elif user.groups.filter(name='Empleados').exists():
                    return redirect('dashboard')
                else:
                    messages.error(request, 'No tiene permisos asignados')
                    return redirect('login')
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Información proporcionada no válida')
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

def user(request):
    return render(request,'user.html')

def dashboard(request):
    return render(request,'dashboard.html')

def productos(request):
    data = {
        'medicamentos': Medicamento.objects.all(),
    }
    return render(request, 'productos.html', data)

def sucursales(request):
    data = {
        'sucursales': Sucursal.objects.all(),
    }
    return render(request, 'sucursales.html', data)

def verificar_inventario_view(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    disponible, inventario = pedido.verificar_inventario()

    if disponible:
        mensaje = "El medicamento está disponible en esta sucursal."
    elif inventario:
        mensaje = f"El medicamento está disponible en la sucursal {inventario.sucursal.numero}."
    else:
        mensaje = "El medicamento no está disponible en ninguna sucursal."
    return render(request, 'verificar_inventario.html', {
        'mensaje': mensaje,
        'traer_de_otra_sucursal': pedido.traer_de_otra_sucursal,
        'pedido': pedido
    })

def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pedidos')  # Redirige a la lista de pedidos
    else:
        form = PedidoForm()
    return render(request, 'crear_pedido.html', {'form': form})

def actualizar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('lista_pedidos')
    else:
        form = PedidoForm(instance=pedido)
    return render(request, 'actualizar_pedido.html', {'form': form, 'pedido': pedido})

def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'lista_pedidos.html', {'pedidos': pedidos})

def crear_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_ventas')  # Redirige a la lista de ventas
    else:
        form = VentaForm()
    return render(request, 'crear_venta.html', {'form': form})

def actualizar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            return redirect('lista_ventas')
    else:
        form = VentaForm(instance=venta)
    return render(request, 'actualizar_venta.html', {'form': form, 'venta': venta})

def lista_ventas(request):
    ventas = Venta.objects.all()
    return render(request, 'lista_ventas.html', {'ventas': ventas})