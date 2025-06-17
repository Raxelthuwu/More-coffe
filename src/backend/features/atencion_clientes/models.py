from django.db import models
from gestion_personal.models import Empleados


class Mesas(models.Model):
    id_mesa = models.AutoField(primary_key=True)
    capacidad = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'mesas'

    def __str__(self):
        return f"Mesa {self.id_mesa}"


class ProductosMenu(models.Model):
    id_producto_menu = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50)
    url_imagen = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'productos_menu'

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"


class Pedidos(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    id_mesa = models.ForeignKey(Mesas, models.DO_NOTHING, db_column='id_mesa')
    id_empleado_mesero = models.ForeignKey(Empleados, models.DO_NOTHING, db_column='id_empleado_mesero')
    fecha_hora_creacion = models.DateTimeField()
    estado = models.CharField(max_length=20)
    comentarios = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pedidos'

    def __str__(self):
        return f"Pedido #{self.id_pedido} - Mesa {self.id_mesa.id_mesa}"


class DetallesPedido(models.Model):
    id_detalle_pedido = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedidos, models.DO_NOTHING, db_column='id_pedido')
    id_producto_menu = models.ForeignKey(ProductosMenu, models.DO_NOTHING, db_column='id_producto_menu')
    cantidad = models.IntegerField()
    precio_unitario_venta = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'detalles_pedido'

    def __str__(self):
        return f"{self.cantidad} x {self.id_producto_menu.nombre} (Pedido #{self.id_pedido.id_pedido})"
