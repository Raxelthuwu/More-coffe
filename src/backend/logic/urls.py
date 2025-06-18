from django.urls import path
from logic.views.login import *

urlpatterns = [ 

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),


]