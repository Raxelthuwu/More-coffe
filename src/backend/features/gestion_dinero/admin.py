from django.contrib import admin
from .models import MetodoPagos, CierresCaja, Pagos, Egresos

@admin.register(MetodoPagos)
class MetodoPagosAdmin(admin.ModelAdmin):
    list_display = ('id_metodo_pago', 'nombre')

@admin.register(CierresCaja)
class CierresCajaAdmin(admin.ModelAdmin):
    list_display = ('id_cierre_caja', 'fecha_apertura', 'monto_inicial', 'fecha_cierre', 'monto_final')

@admin.register(Pagos)
class PagosAdmin(admin.ModelAdmin):
    list_display = ('id_pago', 'id_pedido', 'monto', 'propina', 'fecha_hora_pago')

@admin.register(Egresos)
class EgresosAdmin(admin.ModelAdmin):
    list_display = ('id_egreso', 'descripcion', 'monto', 'fecha_egreso', 'id_empleado')
