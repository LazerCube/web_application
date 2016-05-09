from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from authentication.permissions import is_owner

from friends.models import Friend
from authentication.models import Account

@login_required
def profile(request, username):
    profile = get_object_or_404(Account, username=username)

    are_friends = False
    has_permission = False

    has_permission = is_owner(request, profile)

    if is_owner(request, profile):
        has_permission = True
    else:
        are_friends = Friend.objects.are_friends(request.user, profile)


    context = {
        'user': profile,
        'are_friends': are_friends,
        'has_permission' : has_permission,
    }

    return render(request, 'user_profiles/user_profile.html', context)
