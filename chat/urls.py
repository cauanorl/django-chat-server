from django.urls import path
from . import views


app_name = "chat"

urlpatterns = [
    path('room/', views.ChatView.as_view(), name="chat"),
    path('room/ajax/order/<str:selected>/', views.ChatListFriendsAjax.as_view(), name="list_data_ajax"),
    path('room/ajax/friend-chat/', views.ChatFriendAjax.as_view(), name="html_chat_ajax"),
    path('room/ajax/create-message/', views.CreateMessageAjax.as_view(), name="chat_save_message_ajax")
]
