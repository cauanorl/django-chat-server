from django.urls import path
from . import views


app_name = 'authentication'

urlpatterns = [
    path('', views.AuthLoginView.as_view(), name="login"),
    path('logout/', views.logout, name="logout"),
]
