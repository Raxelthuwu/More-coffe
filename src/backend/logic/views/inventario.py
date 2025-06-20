from decimal import Decimal 
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from logic.models.inventario import (
    ProductosInventario, MovimientosInventario, UnidadesMedida
)
from logic.models.empleados import Empleados
from logic.models.atencion import Pedidos


class VerInventarioView(LoginRequiredMixin, View):
    def get(self, request):
        productos = ProductosInventario.objects.select_related('id_proveedor').all()
        empleado = None
        pedido_id = request.GET.get('pedido_id')  # Obtener pedido_id de la URL si existe
        
        if request.user.is_authenticated:
            empleado = Empleados.objects.filter(usuario=request.user).first()
        
        # Opcional: Si necesitas el objeto Pedido completo
        pedido = None
        if pedido_id:
            pedido = get_object_or_404(Pedidos, pk=pedido_id)

        return render(request, 'inventario/ver_inventario.html', {
            'productos': productos,
            'empleado': empleado,
            'pedido_id': pedido_id,  # Pasar solo el ID es suficiente
            'pedido': pedido  # Opcional si necesitas más datos del pedido
        })
    

class FormularioMovimientoView(LoginRequiredMixin, View):
    """Formulario para crear un movimiento de inventario para un pedido específico."""
    def get(self, request, pedido_id):
        pedido = get_object_or_404(Pedidos, pk=pedido_id)
        productos_inventario = ProductosInventario.objects.all()
        unidades = UnidadesMedida.objects.all()
        return render(request, 'inventario/formulario_movimiento.html', {
            'pedido': pedido,
            'productos_inventario': productos_inventario,
            'unidades': unidades,
        })

    def post(self, request, pedido_id):
        """Recibe los datos para crear un movimiento de inventario."""
        producto_id = request.POST.get('producto_id')
        producto = get_object_or_404(ProductosInventario, pk=producto_id)

        empleado = Empleados.objects.get(usuario=request.user)

        tipo = request.POST.get('tipo_movimiento')  # "entrada" o "salida"
        cantidad = request.POST.get('cantidad')
        unidad_id = request.POST.get('unidad')
        origen_redirect = 'ver_detalle_preparacion'
        pedido = get_object_or_404(Pedidos, pk=pedido_id)

        # Validar cantidad
        try:
            cantidad_decimal = Decimal(cantidad)  # ✅ Ahora como Decimal
        except ValueError:
            messages.error(request, "Cantidad inválida.")
            return redirect(origen_redirect, pedido_id=pedido_id)

        # Verificación de stock para salida
        if tipo == 'salida' and cantidad_decimal > producto.stock_actual:
            messages.error(request, "Stock insuficiente para realizar la salida.")
            return redirect(origen_redirect, pedido_id=pedido_id)

        # Actualizar stock
        if tipo == 'entrada':
            producto.stock_actual += cantidad_decimal
        elif tipo == 'salida':
            producto.stock_actual -= cantidad_decimal
        producto.save()

        # Crear registro de movimiento
        MovimientosInventario.objects.create(
            id_producto_inv=producto,
            id_empleado=empleado,
            id_pedido=pedido,
            id_unidad_id=unidad_id,
            fecha_hora=timezone.now(),
            tipo_movimiento=tipo,
            cantidad=cantidad_decimal
        )

        messages.success(request, f"Movimiento de {tipo} registrado correctamente.")
        return redirect(origen_redirect, pedido_id=pedido_id)
