from django.http import HttpRequest

from django.forms import TextInput

from django.shortcuts import redirect

from django.urls import reverse

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages

from django.views.generic.base import TemplateView, View

from .forms import (
    LoginForm, CreateAccountForm,
    UpdateAccountForm, UserAndProfileAbstractForm)
from authentication.models import Profile


class LoginIsNotRequiredMixin(TemplateView, View):
    """
        Mixin que, quando o usuário já estiver logado,
        o manda para a página "social:list_users"
    """
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
            # Função que cria uma conta e faz login.
            self.create_and_login_user(form, self.request)

            return redirect(reverse('social:list_users'))

        return self.render_to_response({'form': form})

    def create_and_login_user(
            self, form: UserAndProfileAbstractForm, request: HttpRequest):
        username = request.POST.get('username')
        password = request.POST.get('password')
        # A foto que foi escolhida no form
        photo = request.FILES.get('photo')
        profile = form.save(commit=False)

        # Cria o user
        user = User.objects.create_user(
                    username=username, password=password)
        # Define o dono do objeto Profile
        profile.user = user
        profile.photo = photo
        profile.save()

        user = auth.authenticate(
            request, username=username, password=password)

        auth.login(request, user)


class EditProfile(LoginRequiredMixin, TemplateView, View):
    template_name = "authentication/registration/update_account.html"

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return super().dispatch(*args, **kwargs)

        self.user = self.request.user
        self.form = UpdateAccountForm(instance=self.request.user.profile)

        return super().dispatch(*args, **kwargs)

    def get(self, *args, **kwargs):
        self.config_field_username()

        return self.render_to_response({'form': self.form})

    def post(self, *args, **kwargs):
        self.form = UpdateAccountForm(data=self.request.POST)
        self.config_field_username()

        if self.form.is_valid():
            username = self.user.username
            password = self.form.cleaned_data.get('password')

            if password:
                self.set_password_and_login(username, password)

            self.update_profile()
            messages.success(self.request, "Configurações salvas com sucesso!")

        return self.render_to_response({'form': self.form})

    def set_password_and_login(self, username, password):
        self.user.set_password(password)
        self.user.save()

        user = auth.authenticate(
            username=username, password=password)
        auth.login(self.request, user)

    def update_profile(self, *args, **kwargs):
        about_me = self.form.cleaned_data.get('about_me')
        photo = self.request.FILES.get('photo')

        profile = Profile.objects.get(id=self.user.profile.id)
        if photo:
            profile.photo = photo
        profile.about_me = about_me
        profile.save()

    def config_field_username(self, *args, **kwargs):
        username_field = self.form.fields.get('username')
        username_field.widget = TextInput(attrs={
                'placeholder': self.user.username,
                'disabled': True,
            })


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)

    return redirect('authentication:login')
