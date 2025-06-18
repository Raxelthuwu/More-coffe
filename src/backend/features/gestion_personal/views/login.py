from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from django.contrib.auth.models import User

class login_view(View):
    def get(self, request):
        return render(request, 'gestion_personal/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            username = user.username 
        except User.DoesNotExist:
            messages.error(request, 'Correo no registrado.')
            return render(request, 'gestion_personal/login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Credenciales inválidas.')
            return render(request, 'gestion_personal/login.html')



class logout_view(View):
    def get(self, request):
        logout(request)
        return redirect('login')