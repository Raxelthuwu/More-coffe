from django.urls import path
from .views.clientes import (
    SeleccionarMesaView, MostrarMenuView, EnviarPedidoView, CuentaClienteView
)
from .views.mesero import (
    NotificacionesMesasView, TomarMesaView, VerPedidosMeseroView, EnviarPedidoCocinaView,  EntregarPedidoView,
)

from .views.cocinero import VerPedidosCocinaView, PrepararPedidoView, PedidoListoView

urlpatterns = [
    # Cliente
    path('', SeleccionarMesaView.as_view(), name='seleccionar_mesa'),  
    path('menu/', MostrarMenuView.as_view(), name='mostrar_menu'),
    path('enviar/', EnviarPedidoView.as_view(), name='enviar_pedido'),
    path('cuenta/', CuentaClienteView.as_view(), name='ver_cuenta_cliente'),

    # Mesero
    path('mesero/notificaciones/', NotificacionesMesasView.as_view(), name='notificaciones_mesero'),
    path('mesero/tomar/<int:pedido_id>/', TomarMesaView.as_view(), name='tomar_mesa'),
    path('mesero/pedidos/', VerPedidosMeseroView.as_view(), name='ver_pedidos_mesero'),
    path('mesero/enviar-cocina/<int:pedido_id>/', EnviarPedidoCocinaView.as_view(), name='enviar_pedido_cocina'),
    path('mesero/entregar/<int:pedido_id>/', EntregarPedidoView.as_view(), name='entregar_pedido'),
    # Cocinero
    path('cocina/', VerPedidosCocinaView.as_view(), name='ver_pedidos_cocina'),
    path('cocina/preparar/<int:pedido_id>/', PrepararPedidoView.as_view(), name='preparar_pedido'),
    path('cocina/listo/<int:pedido_id>/', PedidoListoView.as_view(), name='pedido_listo'),


]
