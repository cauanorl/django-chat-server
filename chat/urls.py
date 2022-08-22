from django.urls import path
from . import views


app_name = "chat"

urlpatterns = [
    # View chat padrão
    path('room/',
         views.ChatView.as_view(),
         name="chat"),

    # View AJAX que carrega o chat da conversa
    path('room/ajax/friend-chat/',
         views.ChatFriendAjax.as_view(),
         name="html_chat_ajax"),

    # View que cria as mensagens
    path('room/ajax/create-message/',
         views.CreateMessageAjax.as_view(),
         name="chat_save_message_ajax")
]
