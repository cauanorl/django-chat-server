from django.template import Library


register = Library()

@register.filter(name="get_friend")
def get_friend(friend_model, user):
    return friend_model.get_friend(user)
