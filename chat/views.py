from django.views.generic.base import TemplateView, View

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType

from django.http import Http404, HttpResponseForbidden, JsonResponse

from django.shortcuts import get_object_or_404
from django.shortcuts import render

from authentication.models import Friend
from .models import MessageTextType, Message


# Create your views here.
class AjaxRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        # Salva na váriavel se a requisição é do tipo AJAX
        is_ajax = self.request.headers.get(
                        'x-requested-with') == 'XMLHttpRequest'

        # Se não for, entrega uma página 404
        if not is_ajax:
            return Http404()

        return super().dispatch(request, *args, **kwargs)


class ChatView(LoginRequiredMixin, TemplateView, View):
    """
    Essa view é o chat default, sem estar com nenhum usuário
    """
    template_name = "chat/room/room.html"

    def get(self, request):
        # Todos os amigos
        self.all_friends = request.user.profile.friends.all()

        # Todas as amizades que foram aceitas
        self.all_accepted_friends = self.all_friends.filter(accept=True)

        context = {
            'all_accepted_friends': self.all_accepted_friends,
        }

        return self.render_to_response(context)


class ChatFriendAjax(AjaxRequiredMixin, View):
    """
    Essa view carrega o chat de forma assíncrona com ajax.
    """
    def post(self, request, *args, **kwargs):
        context = {}

        friend_id = self.request.POST.get('friend_id')
        friend_object = get_object_or_404(Friend, id=friend_id)

        # Retorna o "user_one" ou "user_two" do modelo Friend
        friend = friend_object.get_friend(self.request.user)

        # Verifica se a amizade existe, senão bloqueia a View
        if friend is None:
            return HttpResponseForbidden()

        # Todas as mensagens salvas para carrega-las no Chat
        messages = friend_object.chat_messages.all()

        context.update({
            'messages': messages,
            'friend': friend,
            'friend_object': friend_object,
        })

        return render(request, "chat/ajax_html/_friend_chat.html", context)


class CreateMessageAjax(AjaxRequiredMixin, View):
    """
    Essa view salva as mensagens no banco de dados
    """
    def post(self, request, *args, **kwargs):
        friend_model_id = self.request.POST.get('friend_model_id')
        self.user = self.request.user
        self.type = self.request.POST.get('type')
        self.message = self.request.POST.get('message')

        # verifica que tipo de mensagem é (Texto, Imagem, Video, Arquivo)
        match self.type:
            case "text":
                self.create_text_message(friend_model_id)
            case _:
                ...  # TODO: Criar envio de imagens

        return JsonResponse({'status': "OK"})

    def create_text_message(self, friend_model_id, *args, **kwargs):
        """
        Cria o objeto Message
        """
        friend_object = Friend.objects.get(id=friend_model_id)

        content = MessageTextType.objects.create(content=self.message)
        target_ct = ContentType.objects.get_for_model(MessageTextType)
        target_id = content.id

        Message.objects.create(
            owner=self.user,
            friend_model=friend_object,
            target_ct=target_ct,
            target_id=target_id,
        )
