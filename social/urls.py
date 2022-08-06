from django.urls import path
from . import views


app_name = "social"

urlpatterns = [
    path('', views.UserListView.as_view(), name="list_users"),
    path('friend-request/<int:friend_id>/', views.CreateSolicitationInviteView.as_view(), name="friend_request"),
    path('friend-request-response/<int:model_friend_id>', views.ResponseFriendRequestView.as_view(), name="response_friend")
]
