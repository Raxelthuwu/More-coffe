from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from logic.models.inventario import ProductosInventario, MovimientosInventario, UnidadesMedida, Proveedores
from logic.models.empleados import Empleados, Turnos
from django.http import HttpResponseForbidden

class InicioAdministradorView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'administrador/inicio_administrador.html')


# INVENTARIO
class VerHistorialMovimientosView(LoginRequiredMixin, View):
    def get(self, request):
        movimientos = MovimientosInventario.objects.select_related('id_producto_inv', 'id_empleado', 'id_unidad').order_by('-fecha_hora')
        return render(request, 'inventario/ver_historial_movimientos.html', {'movimientos': movimientos})


class CrearProductoInventarioView(LoginRequiredMixin, View):
    def get(self, request):
        unidades = UnidadesMedida.objects.all()
        proveedores = Proveedores.objects.filter(activo=True)
        return render(request, 'administrador/crear_producto.html', {'unidades': unidades, 'proveedores': proveedores})

    def post(self, request):
        nombre = request.POST.get('nombre')
        unidad_medida = request.POST.get('unidad_medida')
        proveedor_id = request.POST.get('proveedor_id')
        stock_actual = request.POST.get('stock_actual')
        stock_minimo = request.POST.get('stock_minimo')
        stock_maximo = request.POST.get('stock_maximo')

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
        proveedores = Proveedores.objects.filter(activo=True)
        return render(request, 'administrador/editar_producto.html', {'producto': producto, 'unidades': unidades, 'proveedores': proveedores})

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
        empleado = getattr(request.user, 'empleado', None)
        producto = get_object_or_404(ProductosInventario, pk=producto_id)
        producto.activo = False
        producto.save()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('ver_inventario')



# EMPLEADOS
class ListarEmpleadosView(LoginRequiredMixin, View):
    def get(self, request):
        empleados = Empleados.objects.select_related('usuario').filter(activo=True)
        return render(request, 'administrador/listar_empleados.html', {'empleados': empleados})


class CrearEmpleadoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'administrador/crear_empleado.html')

    def post(self, request):
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        password = request.POST.get('password')
        id_rol = request.POST.get('id_rol')

        if not all([nombre, apellido, correo, telefono, password, id_rol]):
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('crear_empleado')

        if Empleados.objects.filter(correo=correo).exists() or User.objects.filter(email=correo).exists():
            messages.error(request, "El correo ya está registrado.")
            return redirect('crear_empleado')

        if Empleados.objects.filter(telefono=telefono).exists():
            messages.error(request, "El teléfono ya está registrado.")
            return redirect('crear_empleado')

        try:
            user = User.objects.create_user(username=correo, email=correo, password=password)
        except Exception as e:
            messages.error(request, "Error al crear el usuario.")
            return redirect('crear_empleado')

        try:
            Empleados.objects.create(
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                telefono=telefono,
                contrasena_hash=user.password,
                id_rol_id=id_rol,
                usuario=user,
                activo=True
            )
        except Exception as e:
            user.delete()
            messages.error(request, "Error al crear el empleado.")
            return redirect('crear_empleado')

        messages.success(request, "Empleado creado exitosamente.")
        return redirect('listar_empleados')


class EditarEmpleadoView(LoginRequiredMixin, View):
    def get(self, request, empleado_id):
        empleado = get_object_or_404(Empleados, pk=empleado_id)
        return render(request, 'administrador/editar_empleado.html', {'empleado': empleado})

    def post(self, request, empleado_id):
        empleado = get_object_or_404(Empleados, pk=empleado_id)
        usuario = empleado.usuario

        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        rol_id = request.POST.get('rol')
        nueva_password = request.POST.get('password')

        if correo != empleado.correo:
            if Empleados.objects.filter(correo=correo).exclude(pk=empleado.pk).exists() or \
               User.objects.filter(email=correo).exclude(pk=usuario.pk).exists():
                messages.error(request, "El correo ya está registrado por otro usuario.")
                return redirect('editar_empleado', empleado_id=empleado_id)
            empleado.correo = correo
            usuario.email = correo
            usuario.username = correo

        if telefono != empleado.telefono:
            if Empleados.objects.filter(telefono=telefono).exclude(pk=empleado.pk).exists():
                messages.error(request, "El teléfono ya está registrado por otro usuario.")
                return redirect('editar_empleado', empleado_id=empleado_id)
            empleado.telefono = telefono

        empleado.nombre = nombre
        empleado.apellido = apellido
        empleado.id_rol_id = rol_id

        if nueva_password:
            usuario.set_password(nueva_password)
            usuario.save()
            empleado.contrasena_hash = usuario.password

        usuario.save()
        empleado.save()

        messages.success(request, "Empleado actualizado correctamente.")
        return redirect('listar_empleados')


class EliminarEmpleadoView(LoginRequiredMixin, View):
    def post(self, request, empleado_id):
        empleado = get_object_or_404(Empleados, pk=empleado_id)
        user = empleado.usuario
        empleado.activo = False
        empleado.save()
        if user:
            user.is_active = False
            user.save()
        messages.success(request, "Empleado eliminado correctamente.")
        return redirect('listar_empleados')


# PROVEEDORES
class ListarProveedoresView(LoginRequiredMixin, View):
    def get(self, request):
        proveedores = Proveedores.objects.filter(activo=True)
        return render(request, 'administrador/listar_proveedores.html', {'proveedores': proveedores})


class CrearProveedorView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'administrador/crear_proveedor.html')

    def post(self, request):
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')

        if not nombre or not telefono:
            messages.error(request, "Nombre y teléfono son obligatorios.")
            return redirect('crear_proveedor')

        Proveedores.objects.create(nombre=nombre, telefono=telefono, correo=correo)
        messages.success(request, "Proveedor creado correctamente.")
        return redirect('listar_proveedores')


class EditarProveedorView(LoginRequiredMixin, View):
    def get(self, request, proveedor_id):
        proveedor = get_object_or_404(Proveedores, pk=proveedor_id)
        return render(request, 'administrador/editar_proveedor.html', {'proveedor': proveedor})

    def post(self, request, proveedor_id):
        proveedor = get_object_or_404(Proveedores, pk=proveedor_id)
        proveedor.nombre = request.POST.get('nombre')
        proveedor.telefono = request.POST.get('telefono')
        proveedor.correo = request.POST.get('correo')
        proveedor.save()
        messages.success(request, "Proveedor actualizado correctamente.")
        return redirect('listar_proveedores')


class EliminarProveedorView(LoginRequiredMixin, View):
    def post(self, request, proveedor_id):
        proveedor = get_object_or_404(Proveedores, pk=proveedor_id)
        proveedor.activo = False
        proveedor.save()
        messages.success(request, "Proveedor eliminado correctamente.")
        return redirect('listar_proveedores')


# TURNOS
class ListarTurnosView(LoginRequiredMixin, View):
    def get(self, request):
        turnos = Turnos.objects.select_related('id_empleado').order_by('-hora_entrada')
        return render(request, 'administrador/listar_turnos.html', {'turnos': turnos})
