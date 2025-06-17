from django.contrib import admin
from .models import Roles, Empleados, Turnos

@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    list_display = ('id_rol', 'nombre_rol')

@admin.register(Empleados)
class EmpleadosAdmin(admin.ModelAdmin):
    list_display = ('id_empleado', 'nombre', 'apellido', 'telefono', 'correo', 'id_rol')
    search_fields = ('nombre', 'apellido', 'correo')

@admin.register(Turnos)
class TurnosAdmin(admin.ModelAdmin):
    list_display = ('id_turno', 'id_empleado', 'hora_entrada', 'hora_salida')
