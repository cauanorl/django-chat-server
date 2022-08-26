from django import forms
from django.contrib.auth.models import User

from django.contrib import auth


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Nome de usuário...'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Senha...'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not User.objects.filter(username=username).exists():
            self.add_error('username', forms.ValidationError("Nome de usuário não existe."))
            return

        user = auth.authenticate(username=username, password=password)

        if user is None:
            self.add_error('password', forms.ValidationError("A senha está incorreta."))

        return super().clean()


# CreateProfile
# def clean_password(self, *args, **kwargs):
#     password = self.cleaned_data.get('password')
    
#     if password > 50:
#         self.add_error('password', forms.ValidationError("A senha é muito grande."))
    
#     if password < 8:
#         self.add_error('password', forms.ValidationError("A senha deve ter mais que 8 caracteres."))
    
#     continuos_password = [v+1 for v in password]
    
#     if password == continuos_password:
#         self.add_error('password', forms.ValidationError('Senha não pode ser sequêncial.'))

#     return password
