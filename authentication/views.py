from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from django.contrib import auth
from django.views.generic.base import TemplateView, View

from .forms import LoginForm


class AuthLoginView(TemplateView, View):
    template_name = "authentication/registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('social:list_users'))

        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        
        return self.render_to_response({'form': form})
    
    def post(self, request, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        form = LoginForm(self.request.POST)
        
        if form.is_valid():
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)

                return redirect(reverse('social:list_users'))

        return self.render_to_response({'form': form})
        


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)

    return redirect('authentication:login')
