
from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(
                    max_length=30,
                    widget=forms.TextInput(
                            attrs={
                                    'placeholder': 'Nome de usuário...'
                                }))

    password = forms.CharField(
                        max_length=50,
                        widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Senha...'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not User.objects.filter(username=username).exists():
            self.add_error(
                'username', forms.ValidationError(
                                    "Nome de usuário não existe."))
            return

        user = auth.authenticate(username=username, password=password)

        if user is None:
            self.add_error(
                'password', forms.ValidationError("A senha está incorreta."))

        return super().clean()


class UserAndProfileAbstractForm(forms.ModelForm):
    """
        Form que cria uma conta.
        Validações feitas até agora:
            Username:
                Tem que ser unico
                Tem que ter mais de 5 caracteres
            Password:
                Tem que ter mais de 7 caracteres e menos que 50
                Tem que condizer com a senha do campo "repeat_password"
        Campos obrigatórios:
            username
            password
            repeat_password
    """
    class Meta:
        abstract = True
        model = Profile
        fields = ['username', 'password',
                  'repeat_password', 'about_me', 'photo']

    username = forms.CharField(
                    max_length=30,
                    widget=forms.TextInput(
                            attrs={'placeholder': 'Nome de usuário...'}))

    password = forms.CharField(
                    max_length=50,
                    widget=forms.PasswordInput(
                            attrs={'placeholder': 'Senha...'}))

    repeat_password = forms.CharField(
                    max_length=50,
                    widget=forms.PasswordInput(
                            attrs={'placeholder': 'Confirmar senha...'}))

    about_me = forms.CharField(
                    max_length=500,
                    required=False,
                    widget=forms.Textarea({'placeholder': 'Sobre mim...'}))

    def clean_password(self, *args, **kwargs):
        password = self.cleaned_data.get('password')

        if len(password) > 50:
            self.add_error(
                'password',
                forms.ValidationError("A senha é muito grande."))

        if len(password) < 8:
            self.add_error(
                'password',
                forms.ValidationError(
                    "A senha deve ter mais que 8 caracteres."))

        # if password == continuos_password:
        #     self.add_error(
        #         'password',
        #         forms.ValidationError('Senha não pode ser sequêncial.'))

        return password

    def clean_repeat_password(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')

        if password != repeat_password:
            self.add_error(
                'repeat_password',
                forms.ValidationError("As senhas não conferem."))

        return repeat_password

    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            self.add_error(
                'username', forms.ValidationError("Nome de usuário já existe"))

        if len(username) < 6:
            self.add_error(
                'username',
                forms.ValidationError(
                    'Nome de usuário não pode ter menos que 6 caracteres.'))

        return username


class CreateAccountForm(UserAndProfileAbstractForm):
    ...


class UpdateAccountForm(UserAndProfileAbstractForm):
    class Meta:
        model = Profile
        fields = ['username', 'password', 'repeat_password',
                  'about_me', 'photo']

    username = forms.CharField(
                    max_length=30,
                    required=False,
                    widget=forms.TextInput(
                            attrs={
                                'placeholder': 'Nome de usuário...',
                                'disabled': True,
                            }))

    password = forms.CharField(
                    max_length=50,
                    required=False,
                    widget=forms.PasswordInput(
                            attrs={'placeholder': 'Nova senha...'}))

    repeat_password = forms.CharField(
                    max_length=50,
                    required=False,
                    widget=forms.PasswordInput(
                            attrs={'placeholder': 'Confirmar senha...'}))

    def clean_username(self, *args, **kwargs):
        return False

    def clean_repeat_password(self, *args, **kwargs):
        repeat_password = self.cleaned_data.get('repeat_password')
        password = self.cleaned_data.get('password')

        if not repeat_password and not password:
            return False

        return super().clean_repeat_password(*args, **kwargs)

    def clean_password(self, *args, **kwargs):
        password = self.cleaned_data.get('password')

        if not password:
            return None

        return super().clean_password(*args, **kwargs)
