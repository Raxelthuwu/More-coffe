from django.contrib import admin
from .models import MetodoPagos, Pagos, Egresos, CierresCaja

@admin.register(MetodoPagos)
class MetodoPagosAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Pagos)
class PagosAdmin(admin.ModelAdmin):
    list_display = ('id_pedido', 'id_empleado_cajero', 'monto', 'propina', 'fecha_hora_pago')

@admin.register(Egresos)
class EgresosAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'monto', 'fecha_egreso', 'id_empleado')

@admin.register(CierresCaja)
class CierresCajaAdmin(admin.ModelAdmin):
    list_display = ('fecha_apertura', 'fecha_cierre', 'monto_inicial', 'monto_final')
