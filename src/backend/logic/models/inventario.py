from django.db import models
from .empleados import Empleados
from .atencion import Pedidos  


class Proveedores(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=60)
    telefono = models.CharField(max_length=20)
    correo = models.CharField(max_length=80, blank=True, null=True)
    activo = models.BooleanField(default=True)  # <-- campo agregado

    class Meta:
        managed = False
        db_table = 'proveedores'

    def __str__(self):
        return self.nombre


class UnidadesMedida(models.Model):
    id_unidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'unidades_medida'

    def __str__(self):
        return self.nombre


class ProductosInventario(models.Model):
    id_producto_inv = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=100)
    id_proveedor = models.ForeignKey(Proveedores, models.DO_NOTHING, db_column='id_proveedor', blank=True, null=True)
    unidad_medida = models.CharField(max_length=20)
    stock_actual = models.DecimalField(max_digits=10, decimal_places=1)
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=1)
    stock_maximo = models.DecimalField(max_digits=10, decimal_places=1)
    activo = models.BooleanField(default=True)  

    class Meta:
        managed = False
        db_table = 'productos_inventario'

    def __str__(self):
        return self.nombre


class MovimientosInventario(models.Model):
    id_movimiento = models.AutoField(primary_key=True)
    id_producto_inv = models.ForeignKey(ProductosInventario, models.DO_NOTHING, db_column='id_producto_inv')
    id_empleado = models.ForeignKey(Empleados, models.DO_NOTHING, db_column='id_empleado')
    id_pedido = models.ForeignKey(Pedidos, models.DO_NOTHING, db_column='id_pedido', blank=True, null=True)
    id_unidad = models.ForeignKey(UnidadesMedida, models.DO_NOTHING, db_column='id_unidad')
    fecha_hora = models.DateTimeField()
    tipo_movimiento = models.CharField(max_length=10)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'movimientos_inventario'

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.id_producto_inv.nombre} ({self.fecha_hora})"
