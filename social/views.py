from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from django.contrib.auth.models import User

from django.views.generic.list import ListView
from django.views.generic.base import TemplateResponseMixin, View

from django.contrib.auth.mixins import LoginRequiredMixin

from authentication.models import Friend
from chat.models import Message


# Create your views here.
class UserListView(LoginRequiredMixin, ListView):
    template_name = "social/users/list.html"
    model = User
    context_object_name = "users"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        # Exclui o usuário que enviou a solicitação e o próprio
        qs = qs.exclude(id=self.request.user.id) \
               .exclude(profile__friends__user_one=self.request.user)

        return qs


class CreateSolicitationInviteView(LoginRequiredMixin, TemplateResponseMixin, View):
    """
    Classe que envia a solicitação de amizade
    """
    def post(self, request, friend_id, *args, **kwargs):
        user = self.request.user
        # Seleciona o usuário que receberá a solicitação
        other_user = get_object_or_404(User, id=friend_id)

        # Cria um objeto Friend onde user_one é quem enviou a solicitação
        friend = Friend.objects.create(
            user_one=user,
            user_two=other_user,
        )

        #  Adiciona o objeto Friend aos usuários que se conectarão,
        #  independente se o pedido foi aceito ou não
        other_user.profile.friends.add(friend)
        user.profile.friends.add(friend)

        return HttpResponse('Ok')


class ResponseFriendRequestView(TemplateResponseMixin, View):
    """
    Classe que, quando o usuário clicar em aceitar um pedido de amizade ou 
    recusar, fará o tratamento nescessário e fará uma ligação entre os dois
    usuários
    """
    def post(self, request, model_friend_id, *args, **kwargs):
        friend = get_object_or_404(Friend, id=model_friend_id)
        # Recebe a resposta do pedido como "accept" ou "refuse"
        response = self.request.POST.get('accept')  

        if response == "accept":
            friend.accept = True  # Aceita o pedido
            friend.save()
        elif response == "refuse":
            friend.delete()  # Recusa o pedido

        return redirect(reverse("chat:chat"))
