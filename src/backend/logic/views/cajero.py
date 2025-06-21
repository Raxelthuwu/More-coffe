from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from logic.models.atencion import Pedidos, DetallesPedido
from logic.models.pagos import MetodoPagos, Pagos
from logic.models.empleados import Empleados
from logic.models.pagos import CierresCaja
from decimal import Decimal, InvalidOperation


class VerPedidosCajeroView(LoginRequiredMixin, View):
    def get(self, request):
        pedidos = Pedidos.objects.filter(estado='entregado')  # Solo pedidos entregados
        return render(request, 'cajero/ver_pedidos_cajero.html', {  
            'pedidos': pedidos
        })


class VerDetallePedidoCajeroView(LoginRequiredMixin, View):
    def get(self, request, pedido_id):
        pedido = get_object_or_404(Pedidos, pk=pedido_id)

        if pedido.estado != 'entregado':
            messages.error(request, "El pedido no está listo para pagar.")
            return redirect('ver_pedidos_cajero')

        detalles = DetallesPedido.objects.filter(id_pedido=pedido)
        metodos_pago = MetodoPagos.objects.all()

        # Calcula el total del pedido
        total = sum(detalle.precio_total for detalle in detalles)

        return render(request, 'cajero/ver_detalle_pedido_cajero.html', { 
            'pedido': pedido,
            'detalles': detalles,
            'metodos_pago': metodos_pago,
            'total': total
        })


class RegistrarPagoPedidoView(LoginRequiredMixin, View):
    def post(self, request, pedido_id):
        pedido = get_object_or_404(Pedidos, pk=pedido_id)

        if pedido.estado != 'entregado':
            messages.error(request, "El pedido no está listo para pagarse.")
            return redirect('ver_pedidos_cajero')

        cajero = Empleados.objects.get(usuario=request.user)
        metodo_id = request.POST.get('metodo_pago')
        propina = request.POST.get('propina') or 0

        try:
            propina = Decimal(propina)
        except (InvalidOperation, TypeError):
            messages.error(request, "Propina inválida.")
            return redirect('ver_detalle_pedido_cajero', pedido_id=pedido.id_pedido)

        detalles = DetallesPedido.objects.filter(id_pedido=pedido)
        total = sum(detalle.precio_total for detalle in detalles)

        for detalle in detalles:
            Pagos.objects.create(
                id_empleado_cajero=cajero,
                monto=detalle.precio_total,
                propina=propina,
                id_metodo_pago_id=metodo_id,
                fecha_hora_pago=timezone.now(),
                id_detalle_pedido=detalle
            )

        pedido.estado = 'pagado'
        pedido.save()

        messages.success(request, "Pago registrado correctamente. Total pagado: ${}".format(total))
        return redirect('ver_pedidos_cajero')


class AperturaCajaView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'cajero/apertura_caja.html') 

    def post(self, request):
        empleado = Empleados.objects.get(usuario=request.user)

        caja_abierta = CierresCaja.objects.filter(
            id_empleado_apertura=empleado,
            fecha_cierre__isnull=True
        ).first()

        if caja_abierta:
            messages.error(request, "Ya tienes una caja abierta.")
            return redirect('apertura_caja')

        monto_inicial = request.POST.get('monto_inicial')
        try:
            monto_inicial = float(monto_inicial)
        except ValueError:
            messages.error(request, "Monto inválido.")
            return redirect('apertura_caja')

        CierresCaja.objects.create(
            fecha_apertura=timezone.now(),
            monto_inicial=monto_inicial,
            id_empleado_apertura=empleado
        )

        messages.success(request, "Caja abierta correctamente.")
        return redirect('ver_pedidos_cajero')


class CierreCajaView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'cajero/cierre_caja.html')  
    def post(self, request):
        empleado = Empleados.objects.get(usuario=request.user)

        caja = CierresCaja.objects.filter(
            id_empleado_apertura=empleado,
            fecha_cierre__isnull=True
        ).first()

        if not caja:
            messages.error(request, "No tienes ninguna caja abierta.")
            return redirect('cierre_caja')

        monto_final = request.POST.get('monto_final')
        try:
            monto_final = Decimal(monto_final)
        except (InvalidOperation, TypeError):
            messages.error(request, "Monto inválido.")
            return redirect('cierre_caja')

        caja.fecha_cierre = timezone.now()
        caja.monto_final = monto_final
        caja.id_empleado_cierre = empleado
        caja.save()

        from django.contrib.auth import logout
        logout(request)

        messages.success(request, "Caja cerrada y sesión cerrada correctamente.")
        return redirect('login')
