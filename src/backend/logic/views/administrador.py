from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from logic.models.inventario import ProductosInventario, MovimientosInventario, UnidadesMedida, Proveedores
from logic.models.empleados import Empleados
from django.utils import timezone


class VerHistorialMovimientosView(LoginRequiredMixin, View):
    def get(self, request):
        movimientos = MovimientosInventario.objects.select_related(
            'id_producto_inv', 'id_empleado', 'id_unidad'
        ).order_by('-fecha_hora')

        # Aquí va el HTML para mostrar el historial de movimientos
        return render(request, 'aqui_va_el_html_historial_movimientos.html', {
            'movimientos': movimientos
        })


class CrearProductoInventarioView(LoginRequiredMixin, View):
    def get(self, request):
        unidades = UnidadesMedida.objects.all()
        proveedores = Proveedores.objects.all()

        # Aquí va el HTML del formulario para crear producto
        return render(request, 'aqui_va_el_html_crear_producto.html', {
            'unidades': unidades,
            'proveedores': proveedores
        })

    def post(self, request):
        nombre = request.POST.get('nombre')
        unidad_medida = request.POST.get('unidad_medida')
        proveedor_id = request.POST.get('proveedor_id')
        stock_actual = request.POST.get('stock_actual')
        stock_minimo = request.POST.get('stock_minimo')
        stock_maximo = request.POST.get('stock_maximo')

        # Validación simple
        if not nombre or not stock_actual:
            messages.error(request, "Nombre y stock actual son obligatorios.")
            return redirect('crear_producto_inventario')

        ProductosInventario.objects.create(
            nombre=nombre,
            unidad_medida=unidad_medida,
            id_proveedor_id=proveedor_id if proveedor_id else None,
            stock_actual=stock_actual,
            stock_minimo=stock_minimo or 0,
            stock_maximo=stock_maximo or 0
        )

        messages.success(request, "Producto creado correctamente.")
        return redirect('ver_inventario')


class EditarProductoInventarioView(LoginRequiredMixin, View):
    def get(self, request, producto_id):
        producto = get_object_or_404(ProductosInventario, pk=producto_id)
        unidades = UnidadesMedida.objects.all()
        proveedores = Proveedores.objects.all()

        # HTML para editar producto
        return render(request, 'aqui_va_el_html_editar_producto.html', {
            'producto': producto,
            'unidades': unidades,
            'proveedores': proveedores
        })

    def post(self, request, producto_id):
        producto = get_object_or_404(ProductosInventario, pk=producto_id)

        producto.nombre = request.POST.get('nombre')
        producto.unidad_medida = request.POST.get('unidad_medida')
        producto.id_proveedor_id = request.POST.get('proveedor_id')
        producto.stock_actual = request.POST.get('stock_actual')
        producto.stock_minimo = request.POST.get('stock_minimo')
        producto.stock_maximo = request.POST.get('stock_maximo')
        producto.save()

        messages.success(request, "Producto actualizado correctamente.")
        return redirect('ver_inventario')


class EliminarProductoInventarioView(LoginRequiredMixin, View):
    def post(self, request, producto_id):
        producto = get_object_or_404(ProductosInventario, pk=producto_id)
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('ver_inventario')



class ListarEmpleadosView(LoginRequiredMixin, View):
    def get(self, request):
        empleados = Empleados.objects.select_related('usuario').all()
        # Aquí va el HTML que muestra la lista de empleados
        return render(request, 'aqui_va_el_html_listar_empleados.html', {
            'empleados': empleados
        })


class CrearEmpleadoView(LoginRequiredMixin, View):
    def get(self, request):
        # Aquí va el HTML con el formulario para crear un nuevo empleado
        return render(request, 'aqui_va_el_html_crear_empleado.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        nombre = request.POST.get('nombre')
        rol = request.POST.get('rol')

        if not username or not password or not nombre or not rol:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('crear_empleado')

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
            return redirect('crear_empleado')

        user = User.objects.create_user(username=username, password=password)
        Empleados.objects.create(usuario=user, nombre=nombre, rol=rol)

        messages.success(request, "Empleado creado exitosamente.")
        return redirect('listar_empleados')


class EditarEmpleadoView(LoginRequiredMixin, View):
    def get(self, request, empleado_id):
        empleado = get_object_or_404(Empleados, pk=empleado_id)
        # Aquí va el HTML para editar datos del empleado
        return render(request, 'aqui_va_el_html_editar_empleado.html', {
            'empleado': empleado
        })

    def post(self, request, empleado_id):
        empleado = get_object_or_404(Empleados, pk=empleado_id)

        empleado.nombre = request.POST.get('nombre')
        empleado.rol = request.POST.get('rol')
        empleado.save()

        messages.success(request, "Empleado actualizado correctamente.")
        return redirect('listar_empleados')


class EliminarEmpleadoView(LoginRequiredMixin, View):
    def post(self, request, empleado_id):
        empleado = get_object_or_404(Empleados, pk=empleado_id)
        user = empleado.usuario
        empleado.delete()
        user.delete()
        messages.success(request, "Empleado eliminado correctamente.")
        return redirect('listar_empleados')

class ListarProveedoresView(LoginRequiredMixin, View):
    def get(self, request):
        proveedores = Proveedores.objects.all()
        # Aquí va el HTML que lista todos los proveedores
        return render(request, 'aqui_va_el_html_listar_proveedores.html', {
            'proveedores': proveedores
        })


class CrearProveedorView(LoginRequiredMixin, View):
    def get(self, request):
        # Aquí va el HTML que muestra el formulario para crear proveedor
        return render(request, 'aqui_va_el_html_crear_proveedor.html')

    def post(self, request):
        nombre = request.POST.get('nombre')
        contacto = request.POST.get('contacto')

        if not nombre or not contacto:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('crear_proveedor')

        Proveedores.objects.create(nombre=nombre, contacto=contacto)
        messages.success(request, "Proveedor creado correctamente.")
        return redirect('listar_proveedores')


class EditarProveedorView(LoginRequiredMixin, View):
    def get(self, request, proveedor_id):
        proveedor = get_object_or_404(Proveedores, pk=proveedor_id)
        # Aquí va el HTML que muestra el formulario para editar proveedor
        return render(request, 'aqui_va_el_html_editar_proveedor.html', {
            'proveedor': proveedor
        })

    def post(self, request, proveedor_id):
        proveedor = get_object_or_404(Proveedores, pk=proveedor_id)

        proveedor.nombre = request.POST.get('nombre')
        proveedor.contacto = request.POST.get('contacto')
        proveedor.save()

        messages.success(request, "Proveedor actualizado correctamente.")
        return redirect('listar_proveedores')


class EliminarProveedorView(LoginRequiredMixin, View):
    def post(self, request, proveedor_id):
        proveedor = get_object_or_404(Proveedores, pk=proveedor_id)
        proveedor.delete()
        messages.success(request, "Proveedor eliminado correctamente.")
        return redirect('listar_proveedores')