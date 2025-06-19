from django.test import SimpleTestCase
from django.urls import resolve

# Cliente
from logic.views.cliente import (
    SeleccionarMesaView,
    MostrarMenuView,
    EnviarPedidoView,
    VerPedidoActualView,
    CancelarPedidoView,
    VolverAMenuView,
)

# Mesero
from logic.views.mesero import (
    NotificacionesMesasView,
    DetallePedidoMeseroView,
    TomarMesaView,
    EntregarPedidoView,
    EnviarPedidoCocinaView,
    VerPedidosMeseroView,
)

# Cocinero
from logic.views.cocinero import (
    VerPedidosCocinaView,
    TomarPedidoCocinaView,
    VerDetallePreparacionView,
    RegistrarPreparacionView,
)

# Inventario
from logic.views.inventario import (
    VerInventarioView,
    FormularioMovimientoView,
)

# Administrador
from logic.views.administrador import (
    VerHistorialMovimientosView,
    CrearProductoInventarioView,
    EditarProductoInventarioView,
    EliminarProductoInventarioView,
    ListarEmpleadosView,
    CrearEmpleadoView,
    EditarEmpleadoView,
    EliminarEmpleadoView,
    ListarProveedoresView,
    CrearProveedorView,
    EditarProveedorView,
    EliminarProveedorView,
)

# Cajero
from logic.views.cajero import (
    VerPedidosCajeroView,
    VerDetallePedidoCajeroView,
    RegistrarPagoPedidoView,
    AperturaCajaView,
    CierreCajaView,
)

# Login
from logic.views.login import LoginView, LogoutView


class TestURLs(SimpleTestCase):

    # Login
    def test_login_url(self):
        resolver = resolve('/login/')
        self.assertEqual(resolver.func.view_class, LoginView)

    def test_logout_url(self):
        resolver = resolve('/logout/')
        self.assertEqual(resolver.func.view_class, LogoutView)

    # Cliente
    def test_seleccionar_mesa_url(self):
        resolver = resolve('/')
        self.assertEqual(resolver.func.view_class, SeleccionarMesaView)

    def test_mostrar_menu_url(self):
        resolver = resolve('/menu/')
        self.assertEqual(resolver.func.view_class, MostrarMenuView)

    def test_enviar_pedido_url(self):
        resolver = resolve('/enviar-pedido/')
        self.assertEqual(resolver.func.view_class, EnviarPedidoView)

    def test_ver_cuenta_url(self):
        resolver = resolve('/ver-cuenta/')
        self.assertEqual(resolver.func.view_class, VerPedidoActualView)

    def test_cancelar_pedido_url(self):
        resolver = resolve('/cancelar-pedido/')
        self.assertEqual(resolver.func.view_class, CancelarPedidoView)

    def test_volver_menu_url(self):
        resolver = resolve('/volver-menu/')
        self.assertEqual(resolver.func.view_class, VolverAMenuView)

    # Mesero
    def test_notificaciones_mesas_url(self):
        resolver = resolve('/notificaciones-mesas/')
        self.assertEqual(resolver.func.view_class, NotificacionesMesasView)

    def test_detalle_pedido_mesero_url(self):
        resolver = resolve('/detalle-pedido-mesero/1/')
        self.assertEqual(resolver.func.view_class, DetallePedidoMeseroView)

    def test_tomar_mesa_url(self):
        resolver = resolve('/tomar-mesa/1/')
        self.assertEqual(resolver.func.view_class, TomarMesaView)

    def test_entregar_pedido_url(self):
        resolver = resolve('/entregar-pedido/1/')
        self.assertEqual(resolver.func.view_class, EntregarPedidoView)

    def test_enviar_pedido_cocina_url(self):
        resolver = resolve('/enviar-pedido-cocina/1/')
        self.assertEqual(resolver.func.view_class, EnviarPedidoCocinaView)

    def test_ver_pedidos_mesero_url(self):
        resolver = resolve('/ver-pedidos-mesero/')
        self.assertEqual(resolver.func.view_class, VerPedidosMeseroView)

    # Cocinero
    def test_ver_pedidos_cocina_url(self):
        resolver = resolve('/pedidos-cocina/')
        self.assertEqual(resolver.func.view_class, VerPedidosCocinaView)

    def test_tomar_pedido_cocina_url(self):
        resolver = resolve('/tomar-pedido-cocina/1/')
        self.assertEqual(resolver.func.view_class, TomarPedidoCocinaView)

    def test_ver_detalle_preparacion_url(self):
        resolver = resolve('/detalle-preparacion/1/')
        self.assertEqual(resolver.func.view_class, VerDetallePreparacionView)

    def test_registrar_preparacion_url(self):
        resolver = resolve('/registrar-preparacion/1/')
        self.assertEqual(resolver.func.view_class, RegistrarPreparacionView)

    # Inventario
    def test_ver_inventario_url(self):
        resolver = resolve('/inventario/')
        self.assertEqual(resolver.func.view_class, VerInventarioView)

    def test_formulario_movimiento_url(self):
        resolver = resolve('/inventario/movimiento/1/')
        self.assertEqual(resolver.func.view_class, FormularioMovimientoView)

    # Administrador
    def test_historial_movimientos_url(self):
        resolver = resolve('/inventario/historial/')
        self.assertEqual(resolver.func.view_class, VerHistorialMovimientosView)

    def test_crear_producto_inventario_url(self):
        resolver = resolve('/inventario/crear/')
        self.assertEqual(resolver.func.view_class, CrearProductoInventarioView)

    def test_editar_producto_inventario_url(self):
        resolver = resolve('/inventario/editar/1/')
        self.assertEqual(resolver.func.view_class, EditarProductoInventarioView)

    def test_eliminar_producto_inventario_url(self):
        resolver = resolve('/inventario/eliminar/1/')
        self.assertEqual(resolver.func.view_class, EliminarProductoInventarioView)

    def test_listar_empleados_url(self):
        resolver = resolve('/empleados/')
        self.assertEqual(resolver.func.view_class, ListarEmpleadosView)

    def test_crear_empleado_url(self):
        resolver = resolve('/empleados/crear/')
        self.assertEqual(resolver.func.view_class, CrearEmpleadoView)

    def test_editar_empleado_url(self):
        resolver = resolve('/empleados/editar/1/')
        self.assertEqual(resolver.func.view_class, EditarEmpleadoView)

    def test_eliminar_empleado_url(self):
        resolver = resolve('/empleados/eliminar/1/')
        self.assertEqual(resolver.func.view_class, EliminarEmpleadoView)

    def test_listar_proveedores_url(self):
        resolver = resolve('/proveedores/')
        self.assertEqual(resolver.func.view_class, ListarProveedoresView)

    def test_crear_proveedor_url(self):
        resolver = resolve('/proveedores/crear/')
        self.assertEqual(resolver.func.view_class, CrearProveedorView)

    def test_editar_proveedor_url(self):
        resolver = resolve('/proveedores/editar/1/')
        self.assertEqual(resolver.func.view_class, EditarProveedorView)

    def test_eliminar_proveedor_url(self):
        resolver = resolve('/proveedores/eliminar/1/')
        self.assertEqual(resolver.func.view_class, EliminarProveedorView)

    # Cajero
    def test_ver_pedidos_cajero_url(self):
        resolver = resolve('/cajero/pedidos/')
        self.assertEqual(resolver.func.view_class, VerPedidosCajeroView)

    def test_ver_detalle_pedido_cajero_url(self):
        resolver = resolve('/cajero/pedido/1/detalle/')
        self.assertEqual(resolver.func.view_class, VerDetallePedidoCajeroView)

    def test_registrar_pago_pedido_url(self):
        resolver = resolve('/cajero/pedido/1/pagar/')
        self.assertEqual(resolver.func.view_class, RegistrarPagoPedidoView)

    def test_apertura_caja_url(self):
        resolver = resolve('/cajero/caja/abrir/')
        self.assertEqual(resolver.func.view_class, AperturaCajaView)

    def test_cierre_caja_url(self):
        resolver = resolve('/cajero/caja/cerrar/')
        self.assertEqual(resolver.func.view_class, CierreCajaView)
