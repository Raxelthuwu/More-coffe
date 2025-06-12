from django.contrib import admin
from .models import Mesas, ProductosMenu, Pedidos, DetallesPedido

@admin.register(Mesas)
class MesasAdmin(admin.ModelAdmin):
    list_display = ('numero_mesa', 'capacidad')

@admin.register(ProductosMenu)
class ProductosMenuAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria')
    search_fields = ('nombre',)

@admin.register(Pedidos)
class PedidosAdmin(admin.ModelAdmin):
    list_display = ('id_mesa', 'id_empleado_mesero', 'fecha_hora_creacion', 'estado')

@admin.register(DetallesPedido)
class DetallesPedidoAdmin(admin.ModelAdmin):
    list_display = ('id_pedido', 'id_producto_menu', 'cantidad', 'precio_unitario_venta')
