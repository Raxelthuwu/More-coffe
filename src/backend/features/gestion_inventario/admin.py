from django.contrib import admin
from .models import ProductosInventario, MovimientosInventario, Proveedores, UnidadesMedida

@admin.register(ProductosInventario)
class ProductosInventarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'stock_actual', 'stock_minimo', 'stock_maximo', 'unidad_medida')
    search_fields = ('nombre',)

@admin.register(MovimientosInventario)
class MovimientosInventarioAdmin(admin.ModelAdmin):
    list_display = ('id_producto_inv', 'tipo_movimiento', 'cantidad', 'fecha_hora', 'id_empleado')

@admin.register(Proveedores)
class ProveedoresAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'correo')
    search_fields = ('nombre',)

@admin.register(UnidadesMedida)
class UnidadesMedidaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
