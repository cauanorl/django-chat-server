from django.http import HttpRequest

from django.shortcuts import redirect
from django.urls import reverse

from django.contrib import auth
from django.contrib.auth.models import User

from django.views.generic.base import TemplateView, View

from .forms import LoginForm, CreateAccountForm


class LoginIsNotRequiredMixin(TemplateView, View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('social:list_users'))

        return super().dispatch(request, *args, **kwargs)


class AuthLoginView(LoginIsNotRequiredMixin):
    template_name = "authentication/registration/login.html"

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


class RegistrationView(LoginIsNotRequiredMixin):
    template_name = "authentication/registration/create_account.html"

    def get(self, *args, **kwargs):
        form = CreateAccountForm()

        return self.render_to_response({'form': form})

    def post(self, *args, **kwargs):
        form = CreateAccountForm(self.request.POST)

        if form.is_valid():
            self.create_and_login_user(form, self.request)

            return redirect(reverse('social:list_users'))

        return self.render_to_response({'form': form})

    def create_and_login_user(
            self, form: CreateAccountForm, request: HttpRequest):
        username = request.POST.get('username')
        password = request.POST.get('password')
        photo = request.FILES.get('photo')
        profile = form.save(commit=False)

        user = User.objects.create_user(
                    username=username, password=password)
        profile.user = user
        profile.photo = photo
        profile.save()

        user = auth.authenticate(
            request, username=username, password=password)

        auth.login(request, user)


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)

    return redirect('authentication:login')
