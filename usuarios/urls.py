from django.urls import path
from .views import registro_usuario, login_usuario, logout_usuario, dashboard

urlpatterns = [
    path('registro/', registro_usuario, name='registro'),
    path('login/', login_usuario, name='login'),
    path('logout/', logout_usuario, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
]
