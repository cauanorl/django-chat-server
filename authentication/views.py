from django.shortcuts import redirect
from django.urls import reverse

from django.contrib import auth
from django.contrib.auth.views import LoginView


class AuthLoginView(LoginView):
    template_name = "authentication/registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('social:list_users'))

        return super().dispatch(request, *args, **kwargs)


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)

    return redirect('authentication:login')
