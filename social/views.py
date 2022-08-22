from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User

from django.views.generic.list import ListView
from django.views.generic.base import TemplateResponseMixin, View

from django.contrib.auth.mixins import LoginRequiredMixin

from authentication.models import Friend
from chat.views import AjaxRequiredMixin


class UserListView(LoginRequiredMixin, ListView):
    template_name = "social/users/list.html"
    model = User
    context_object_name = "users"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        # Exclui o usuário que enviou a solicitação e o próprio
        qs = qs.exclude(id=self.request.user.id) \
               .exclude(profile__friends__user_one=self.request.user) \
               .exclude(profile__friends__user_two=self.request.user)

        return qs


class CreateSolicitationInviteView(
            LoginRequiredMixin, TemplateResponseMixin, View):
    """
    Classe que envia a solicitação de amizade
    """
    def post(self, request, *args, **kwargs):
        user = self.request.user
        friend_id = self.request.POST.get('user_id')

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


class ResponseFriendRequestViewAjax(AjaxRequiredMixin, TemplateResponseMixin, View):
    """
    Classe que, quando o usuário clicar em aceitar um pedido de amizade ou
    recusar, fará o tratamento nescessário e fará uma ligação entre os dois
    usuários
    """
    def post(self, request, *args, **kwargs):
        model_friend_id = self.request.POST.get("friend_model_id")

        # Recebe a resposta do pedido como "accept" ou "refuse"
        response = self.request.POST.get('friend_response')

        print(len(response))
        friend = get_object_or_404(Friend, id=model_friend_id)

        if response == "accept":
            friend.accept = True  # Aceita o pedido
            friend.save()
        elif response == "refuse":
            friend.delete()  # Recusa o pedido

        return JsonResponse({'status': 'OK'})


class UpdateNewFriendsRequest(View):
    def get(self, request, *args, **kwargs):
        user = self.request.user

        if not user.is_authenticated:
            return None

        user_friends = user.profile.friends.all()
        user_friends = user_friends.filter(accept=None).exclude(user_one=user)

        return JsonResponse({'user_friends_count': user_friends.count()})
