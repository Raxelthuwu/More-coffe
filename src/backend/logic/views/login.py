from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from logic.models import Empleados


class LoginView(View):
    def get(self, request):
        # Diego aquí se llama al HTML de login con formulario (email, contraseña)
        return render(request, 'login/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        empleado = Empleados.objects.filter(correo=email).first()

        if not empleado or not empleado.usuario:
            messages.error(request, "Credenciales inválidas o usuario no registrado.")
            return redirect('login')

        user = authenticate(request, username=empleado.usuario.username, password=password)

        if user is not None:
            login(request, user)
            rol = empleado.id_rol.nombre_rol.lower()

            if rol == 'mesero':
                return redirect('mesero/mesero.html')  # donde dice esto aqui pone la ruta del HTML, sisa?, si no me pregunta
            elif rol == 'cocinero':
                return redirect('cocina/cocina.html')
            elif rol == 'cajero':
                return redirect('cajero/cajero.html')
            elif rol == 'administrador':
                return redirect('admin/administrador.html')
            else:
                messages.error(request, "Rol no reconocido.")
                return redirect('login')
        else:
            messages.error(request, "Contraseña incorrecta.")
            return redirect('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('Login')  # Redirige a la vista cliente por defecto lo mismo, el HTML de inicio del login 
