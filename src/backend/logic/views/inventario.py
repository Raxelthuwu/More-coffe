from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from logic.models.inventario import (
    ProductosInventario, MovimientosInventario, UnidadesMedida
)
from logic.models.empleados import Empleados



class VerInventarioView(LoginRequiredMixin, View):
    def get(self, request):
        productos = ProductosInventario.objects.select_related('id_proveedor').all()
        # Aquí va el HTML para mostrar el inventario
        return render(request, 'aqui_va_el_html_ver_inventario.html', {
            'productos': productos
        })


class FormularioMovimientoView(LoginRequiredMixin, View):
    def get(self, request, producto_id):
        producto = get_object_or_404(ProductosInventario, pk=producto_id)
        unidades = UnidadesMedida.objects.all()
        pedido_id = request.GET.get('pedido_id')  # opcional, si viene desde cocina

        # Aquí va el HTML del formulario de movimientos de inventario
        return render(request, 'aqui_va_el_html_formulario_movimiento.html', {
            'producto': producto,
            'unidades': unidades,
            'pedido_id': pedido_id
        })

    def post(self, request, producto_id):
        producto = get_object_or_404(ProductosInventario, pk=producto_id)
        empleado = Empleados.objects.get(usuario=request.user)

        tipo = request.POST.get('tipo_movimiento')  # "entrada" o "salida"
        cantidad = request.POST.get('cantidad')
        unidad_id = request.POST.get('unidad')
        pedido_id = request.POST.get('pedido_id')  # opcional

        # Validar cantidad
        try:
            cantidad_decimal = float(cantidad)
        except ValueError:
            messages.error(request, "Cantidad inválida.")
            return redirect('ver_inventario')

        # Verificar si hay stock suficiente si es salida
        if tipo == 'salida' and cantidad_decimal > float(producto.stock_actual):
            messages.error(request, "Stock insuficiente para realizar la salida.")
            return redirect('ver_inventario')

        # Actualizar el stock
        if tipo == 'entrada':
            producto.stock_actual += cantidad_decimal
        elif tipo == 'salida':
            producto.stock_actual -= cantidad_decimal
        producto.save()

        # Crear el movimiento
        MovimientosInventario.objects.create(
            id_producto_inv=producto,
            id_empleado=empleado,
            id_pedido_id=pedido_id if pedido_id else None,
            id_unidad_id=unidad_id,
            fecha_hora=timezone.now(),
            tipo_movimiento=tipo,
            cantidad=cantidad_decimal
        )

        messages.success(request, f"Movimiento de {tipo} registrado correctamente.")

        # Redirigir dependiendo del origen
        if pedido_id:
            return redirect('ver_detalle_preparacion', pedido_id=pedido_id)
        return redirect('ver_inventario')
