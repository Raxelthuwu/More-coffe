from django.db import models
from django.contrib.auth.models import User


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)

    def __str__(self):
        return f"{self.app_label}.{self.model}"


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()

    content_type = models.ForeignKey(
        DjangoContentType, 
        models.DO_NOTHING, 
        blank=True, 
        null=True
    )
    
    user = models.ForeignKey(
        User,  # o Empleados si el admin es del sistema, pero Django usa auth.User
        models.DO_NOTHING
    )

    class Meta:
        managed = False
        db_table = 'django_admin_log'

    def __str__(self):
        return f"{self.action_time} - {self.user}"


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

    def __str__(self):
        return f"Sesión {self.session_key}"


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'

    def __str__(self):
        return f"{self.app} - {self.name}"
