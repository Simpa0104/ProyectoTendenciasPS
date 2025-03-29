from django.urls import path
from .views import registro_usuario, login_usuario, logout_usuario, dashboard

urlpatterns = [
    path('Registro/', registro_usuario, name='registro'),
    path('', login_usuario, name='login'),
    path('Logout/', logout_usuario, name='logout'),
    path('Dashboard/', dashboard, name='dashboard'),
]
