from django.contrib import admin
from django.urls import path, include
from features.atencion_clientes.views.clientes import SeleccionarMesaView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),


    path('', SeleccionarMesaView.as_view(), name='home'),

    
    path('', include("features.atencion_clientes.urls")),
    path('dinero/', include("features.gestion_dinero.urls")),
    path('inventario/', include("features.gestion_inventario.urls")),
    path('personal/', include("features.gestion_personal.urls")),
    path('common/', include("features.common.urls")),
]

