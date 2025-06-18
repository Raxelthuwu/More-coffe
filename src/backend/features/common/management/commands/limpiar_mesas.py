from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session

class Command(BaseCommand):
    help = 'Limpia las sesiones activas relacionadas con mesas ocupadas y pedidos'

    def handle(self, *args, **options):
        sesiones = Session.objects.all()
        contador = 0

        for sesion in sesiones:
            data = sesion.get_decoded()
            if 'mesa_id' in data or 'pedido_id' in data:
                sesion.delete()
                contador += 1

        self.stdout.write(self.style.SUCCESS(f"🧹 Se eliminaron {contador} sesiones relacionadas con mesas/pedidos."))
