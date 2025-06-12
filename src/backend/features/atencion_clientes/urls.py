from django.urls import path
from . import views

urlpatterns = [
    # Cliente
    path('', views.seleccionar_mesa, name='seleccionar_mesa'),
    path('menu/', views.mostrar_menu, name='mostrar_menu'),
    path('enviar-pedido/', views.enviar_pedido, name='enviar_pedido'),
    path('estado-pedido/<int:id_pedido>/', views.ver_estado_pedido, name='ver_estado_pedido'),

    # Mesero
    path('notificaciones-mesas/', views.notificaciones_mesas, name='notificaciones_mesas'),
    path('tomar-mesa/<int:id_pedido>/', views.tomar_mesa, name='tomar_mesa'),
    path('pedidos-mesero/', views.ver_pedidos_mesero, name='ver_pedidos_mesero'),
    path('enviar-a-cocina/<int:id_pedido>/', views.enviar_pedido_cocina, name='enviar_pedido_cocina'),

    # Cocinero
    path('pedidos-cocina/', views.ver_pedidos_cocina, name='ver_pedidos_cocina'),
    path('preparar/<int:id_pedido>/', views.preparar_pedido, name='preparar_pedido'),
    path('marcar-preparado/<int:id_pedido>/', views.marcar_preparado, name='marcar_preparado'),
]