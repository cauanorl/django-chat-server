from django.shortcuts import redirect

from django.contrib import auth
from django.contrib.auth.views import LoginView
 


# Create your views here.
class AuthLoginView(LoginView):
    template_name = "authentication/registration/login.html"


def logout(request):
    auth.logout(request)

    return redirect('authentication:login')
