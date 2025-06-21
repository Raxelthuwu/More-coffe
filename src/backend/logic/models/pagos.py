from django.db import models
from .empleados import Empleados

class MetodoPagos(models.Model):
    id_metodo_pago = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'metodo_pagos'

    def __str__(self):
        return self.nombre


class CierresCaja(models.Model):
    id_cierre_caja = models.AutoField(primary_key=True)
    fecha_apertura = models.DateTimeField()
    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    id_empleado_apertura = models.ForeignKey(Empleados, models.DO_NOTHING, db_column='id_empleado_apertura')
    fecha_cierre = models.DateTimeField(blank=True, null=True)
    monto_final = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    id_empleado_cierre = models.ForeignKey(
        Empleados,
        models.DO_NOTHING,
        db_column='id_empleado_cierre',
        related_name='cierres_caja_cierre',
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'cierres_caja'

    def __str__(self):
        return f"Cierre #{self.id_cierre_caja} - Apertura: {self.fecha_apertura.date()}"


class Pagos(models.Model):
    id_pago = models.AutoField(primary_key=True)
    id_empleado_cajero = models.ForeignKey(
        Empleados,
        on_delete=models.DO_NOTHING,
        db_column='id_empleado_cajero'
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    propina = models.DecimalField(max_digits=10, decimal_places=2)
    id_metodo_pago = models.ForeignKey(
        MetodoPagos,
        on_delete=models.DO_NOTHING,
        db_column='id_metodo_pago'
    )
    fecha_hora_pago = models.DateTimeField()
    id_detalle_pedido = models.ForeignKey(
        'DetallesPedido',
        on_delete=models.DO_NOTHING,
        db_column='id_detalle_pedido'
    )

    class Meta:
        managed = False
        db_table = 'pagos'

    def __str__(self):
        return f"Pago #{self.id_pago} - ${self.monto}"


class Egresos(models.Model):
    id_egreso = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_egreso = models.DateField()
    id_empleado = models.ForeignKey(Empleados, models.DO_NOTHING, db_column='id_empleado')
    id_cierre_caja = models.ForeignKey(
        CierresCaja,
        models.DO_NOTHING,
        db_column='id_cierre_caja',
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'egresos'

    def __str__(self):
        return f"Egreso #{self.id_egreso} - ${self.monto}"
