from django.test import TestCase
from app.models import Mesas, ProductosMenu, Pedidos, DetallesPedido
from gestion_personal.models import Empleados
from django.utils import timezone

class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Configura datos para todas las pruebas"""
        cls.mesa = Mesas.objects.first() or Mesas.objects.create(
            numero_mesa="99",
            capacidad=4
        )
        cls.empleado = Empleados.objects.first()
        cls.producto = ProductosMenu.objects.first() or ProductosMenu.objects.create(
            nombre="Café de prueba",
            precio=5.99,
            categoria="bebida"
        )

    def test_creacion_pedido(self):
        """Prueba la creación de un pedido"""
        pedido = Pedidos.objects.create(
            id_mesa=self.mesa,
            id_empleado_mesero=self.empleado,
            fecha_hora_creacion=timezone.now(),
            estado='en_preparacion'
        )
        self.assertEqual(pedido.id_mesa, self.mesa)
        self.assertEqual(pedido.estado, 'en_preparacion')

    def test_relacion_pedido_detalle(self):
        """Prueba la relación entre pedido y detalles"""
        pedido = Pedidos.objects.create(
            id_mesa=self.mesa,
            id_empleado_mesero=self.empleado,
            fecha_hora_creacion=timezone.now(),
            estado='en_preparacion'
        )
        
        detalle = DetallesPedido.objects.create(
            id_pedido=pedido,
            id_producto_menu=self.producto,
            cantidad=2,
            precio_unitario_venta=self.producto.precio
        )
        
        self.assertEqual(pedido.detallespedido_set.count(), 1)
        self.assertEqual(detalle.id_pedido, pedido)