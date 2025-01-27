from django.contrib import admin
from .models import Empleado,Cliente,Farmacia,Direccion,Sucursal,Inventario,Medicamento,Pedido,Venta,Registro,Stock
from django.contrib import messages

class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre','cedula','telefono','identificacion','salario','rol')
    search_fields = ('nombre','cedula','identificacion')
admin.site.register(Empleado,EmpleadoAdmin)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula', 'telefono')
    search_fields = ('nombre', 'cedula')
admin.site.register(Cliente,ClienteAdmin)
class FarmaciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo')
    search_fields = ('nombre',)
admin.site.register(Farmacia,FarmaciaAdmin)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ('calle_principal', 'calle_secundaria', 'referencia', 'sucursal')
    search_fields = ('sucursal',)
admin.site.register(Direccion,DireccionAdmin)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('numero', 'direccion', 'telefono', 'farmacia')
    search_fields = ('farmacia', 'direccion')
admin.site.register(Sucursal,SucursalAdmin)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'sucursal')
    search_fields = ('codigo',)
admin.site.register(Inventario,InventarioAdmin)
class StockAdmin(admin.ModelAdmin):
    list_display = ('cantidad', 'medicamento','inventario')
admin.site.register(Stock,StockAdmin)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'codigo', 'precio')
    search_fields = ('nombre', 'codigo',)
admin.site.register(Medicamento,MedicamentoAdmin)
def generar_pedido(modeladmin, request, queryset):
    for pedido in queryset:
        disponible, inventario = pedido.verificar_inventario()
        if disponible:
            messages.success(request, f'Pedido realizado en la sucursal actual para el cliente {pedido.cliente}.')
        else:
            if inventario:
                messages.warning(request, f'Pedido no disponible en la sucursal actual. Disponible en sucursal {inventario.sucursal.numero}.')
            else:
                messages.error(request, 'Medicamento no disponible en ninguna sucursal.')

generar_pedido.short_description = 'Generar pedido y verificar inventario'
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'medicamento', 'cantidad', 'venta','traer_de_otra_sucursal')
    search_fields = ('cliente', 'venta')
    actions = [generar_pedido]
admin.site.register(Pedido,PedidoAdmin)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'fecha', 'total', 'tipo_pago', 'registro')
    search_fields = ('codigo', 'tipo_pago')
    readonly_fields = ('total',)
admin.site.register(Venta,VentaAdmin)
admin.site.register(Registro)