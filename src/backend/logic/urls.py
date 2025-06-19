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
    RegistrarPreparacionView,
)

urlpatterns = [ 

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
    path('registrar-preparacion/<int:pedido_id>/', RegistrarPreparacionView.as_view(), name='registrar_preparacion'),



]