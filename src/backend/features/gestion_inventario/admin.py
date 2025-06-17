from django.contrib import admin
from .models import Proveedores, UnidadesMedida, ProductosInventario, MovimientosInventario

@admin.register(Proveedores)
class ProveedoresAdmin(admin.ModelAdmin):
    list_display = ('id_proveedor', 'nombre', 'telefono', 'correo')

@admin.register(UnidadesMedida)
class UnidadesMedidaAdmin(admin.ModelAdmin):
    list_display = ('id_unidad', 'nombre')

@admin.register(ProductosInventario)
class ProductosInventarioAdmin(admin.ModelAdmin):
    list_display = ('id_producto_inv', 'nombre', 'stock_actual', 'stock_minimo', 'stock_maximo', 'unidad_medida')

@admin.register(MovimientosInventario)
class MovimientosInventarioAdmin(admin.ModelAdmin):
    list_display = ('id_movimiento', 'id_producto_inv', 'tipo_movimiento', 'cantidad', 'fecha_hora')
