from django.urls import path
from . import views


app_name = "social"

urlpatterns = [
    path('',
         views.UserListView.as_view(),
         name="list_users"),

    path('friend-request/',
         views.CreateSolicitationInviteView.as_view(),
         name="friend_request"),

    path('friend-request-response/',
         views.ResponseFriendRequestViewAjax.as_view(),
         name="response_friend"),

    path('ajax-count-friend-requests/',
         views.UpdateNewFriendsRequest.as_view(),
         name="count_request_view"),
]
