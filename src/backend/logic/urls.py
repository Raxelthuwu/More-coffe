from django.urls import path
from logic.views.login import *

from logic.views.cliente import (
    SeleccionarMesaView,
    MostrarMenuView,
    EnviarPedidoView,
    VerPedidoActualView,
    CancelarPedidoView,
    VolverAMenuView,
)
from logic.views.mesero import (
    NotificacionesMesasView,
    DetallePedidoMeseroView,
    TomarMesaView,
    EntregarPedidoView,
    EnviarPedidoCocinaView,
    VerPedidosMeseroView,
)

from logic.views.cocinero import (
    VerPedidosCocinaView,
    TomarPedidoCocinaView,
    VerDetallePreparacionView,
    FinalizarPedidoCocinaView
)

from logic.views.inventario import (
    VerInventarioView, 
    FormularioMovimientoView,
    )


from logic.views.administrador import (
    InicioAdministradorView,
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
    ListarTurnosView,
)

from logic.views.cajero import (
    VerPedidosCajeroView,
    VerDetallePedidoCajeroView,
    RegistrarPagoPedidoView,
    AperturaCajaView, 
    CierreCajaView,
)



urlpatterns = [ 

    # rutas de login
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # rutas de cliente
    path('', SeleccionarMesaView.as_view(), name='seleccionar_mesa'),
    path('menu/', MostrarMenuView.as_view(), name='mostrar_menu'),
    path('enviar-pedido/', EnviarPedidoView.as_view(), name='enviar_pedido'),
    path('ver-cuenta/', VerPedidoActualView.as_view(), name='ver_cuenta'),
    path('cancelar-pedido/', CancelarPedidoView.as_view(), name='cancelar_pedido'),
    path('volver-menu/', VolverAMenuView.as_view(), name='volver_menu'),


    # rutas de mesero
    path('notificaciones-mesas/', NotificacionesMesasView.as_view(), name='notificaciones_mesero'),
    path('detalle-pedido-mesero/<int:pedido_id>/', DetallePedidoMeseroView.as_view(), name='detalle_pedido_mesero'),
    path('tomar-mesa/<int:pedido_id>/', TomarMesaView.as_view(), name='tomar_mesa'),
    path('entregar-pedido/<int:pedido_id>/', EntregarPedidoView.as_view(), name='entregar_pedido'),
    path('enviar-pedido-cocina/<int:pedido_id>/', EnviarPedidoCocinaView.as_view(), name='enviar_pedido_cocina'),
    path('ver-pedidos-mesero/', VerPedidosMeseroView.as_view(), name='ver_pedidos_mesero'),

     # rutas de cocinero
    path('pedidos-cocina/', VerPedidosCocinaView.as_view(), name='ver_pedidos_cocina'),
    path('tomar-pedido-cocina/<int:pedido_id>/', TomarPedidoCocinaView.as_view(), name='tomar_pedido_cocina'),
    path('detalle-preparacion/<int:pedido_id>/', VerDetallePreparacionView.as_view(), name='ver_detalle_preparacion'),
    path('finalizar-pedido-cocina/<int:pedido_id>/', FinalizarPedidoCocinaView.as_view(), name='finalizar_pedido_cocina'),


    # rutas de inventario
    path('inventario/', VerInventarioView.as_view(), name='ver_inventario'),
    path('movimientos/', FormularioMovimientoView.as_view(), name='formulario_movimiento'),
    path('movimientos/<int:pedido_id>/', FormularioMovimientoView.as_view(), name='formulario_movimiento_pedido'),




    # Dashboard principal del administrador
    path('panel-administrador/', InicioAdministradorView.as_view(), name='inicio_administrador'),

    # Inventario - Historial de movimientos
    path('administrador/inventario/historial/', VerHistorialMovimientosView.as_view(), name='historial_movimientos'),

    # Inventario - CRUD de productos
    path('administrador/inventario/productos/crear/', CrearProductoInventarioView.as_view(), name='crear_producto_inventario'),
    path('administrador/inventario/productos/editar/<int:producto_id>/', EditarProductoInventarioView.as_view(), name='editar_producto_inventario'),
    path('administrador/inventario/productos/eliminar/<int:producto_id>/', EliminarProductoInventarioView.as_view(), name='eliminar_producto_inventario'),

    # Empleados - CRUD
    path('administrador/empleados/', ListarEmpleadosView.as_view(), name='listar_empleados'),
    path('administrador/empleados/crear/', CrearEmpleadoView.as_view(), name='crear_empleado'),
    path('administrador/empleados/editar/<int:empleado_id>/', EditarEmpleadoView.as_view(), name='editar_empleado'),
    path('administrador/empleados/eliminar/<int:empleado_id>/', EliminarEmpleadoView.as_view(), name='eliminar_empleado'),

    # Proveedores - CRUD
    path('administrador/proveedores/', ListarProveedoresView.as_view(), name='listar_proveedores'),
    path('administrador/proveedores/crear/', CrearProveedorView.as_view(), name='crear_proveedor'),
    path('administrador/proveedores/editar/<int:proveedor_id>/', EditarProveedorView.as_view(), name='editar_proveedor'),
    path('administrador/proveedores/eliminar/<int:proveedor_id>/', EliminarProveedorView.as_view(), name='eliminar_proveedor'),
    # Turnos - CRUD
    path('administrador/turnos/', ListarTurnosView.as_view(), name='listar_turnos'),



    # rutas de cajero
    path('cajero/pedidos/', VerPedidosCajeroView.as_view(), name='ver_pedidos_cajero'),
    path('cajero/pedido/<int:pedido_id>/detalle/', VerDetallePedidoCajeroView.as_view(), name='ver_detalle_pedido_cajero'),
    path('cajero/pedido/<int:pedido_id>/pagar/', RegistrarPagoPedidoView.as_view(), name='registrar_pago_pedido'),
    path('cajero/caja/abrir/', AperturaCajaView.as_view(), name='apertura_caja'),
    path('cajero/caja/cerrar/', CierreCajaView.as_view(), name='cierre_caja'),


]



