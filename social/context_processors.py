def actual_user_friend_requests(request, *args, **kwargs):
    """
    Retorna os users que não foram aceitos aindas e os que estão em
    espera (Pedidos enviados pelo user atual).
    """
    if not request.user.is_authenticated:
        return {}

    user = request.user

    user_friends = user.profile.friends.all()

    friend_requests = user_friends.filter(accept=None).exclude(user_one=user)
    waiting_friend_requests = user_friends.filter(accept=None, user_one=user)

    return {
        'friend_requests': friend_requests,
        'waiting_friend_requests': waiting_friend_requests
    }
