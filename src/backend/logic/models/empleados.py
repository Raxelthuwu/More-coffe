from django.db import models
from django.contrib.auth.models import User


class Roles(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'roles'

    def __str__(self):
        return self.nombre_rol


class Empleados(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(unique=True, max_length=25)
    correo = models.CharField(unique=True, max_length=100)
    id_rol = models.ForeignKey(Roles, models.DO_NOTHING, db_column='id_rol')
    contrasena_hash = models.CharField(max_length=255)
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column='usuario_id'
    )

   
    activo = models.BooleanField(default=True)

    class Meta:
        managed = False  
        db_table = 'empleados'


class Turnos(models.Model):
    id_turno = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(Empleados, models.DO_NOTHING, db_column='id_empleado')
    hora_entrada = models.DateTimeField()
    hora_salida = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'turnos'

    def __str__(self):
        return f"Turno de {self.id_empleado.nombre} ({self.hora_entrada})"
