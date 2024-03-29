from django.urls import path
from . import views


app_name = 'authentication'

urlpatterns = [
    path('', views.AuthLoginView.as_view(), name="login"),
    path('register/', views.RegistrationView.as_view(), name="registration"),
    path('logout/', views.logout, name="logout"),
    path('update/', views.EditProfile.as_view(), name="update_account")
]
