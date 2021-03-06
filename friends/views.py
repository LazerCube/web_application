from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from authentication.permissions import is_owner
from friends.exceptions import AlreadyExistsError

from authentication.models import Account
from models import Friend, FriendRequest

from django.http import HttpResponse
from django.template.loader import render_to_string
import json

@login_required
def list_friends(request):
    '''returns html element for lising friends'''
    if request.method == 'POST':
        response_data = {}

        user = request.user
        friends = Friend.objects.friends(user)

        content = {
            'friends': friends,
        }

        response_data = render_to_string('friends/includes/friends.html', content)
        return HttpResponse(response_data)
    else:
        return HttpResponse(
            json.dumps({ Error : "Something went wrong."}),
            content_type="application/json"
        )


@login_required
def view_friends(request):
    user = request.user
    friends = Friend.objects.friends(user)
    return render(request, 'friends/view_friends.html', {'friends': friends})

@login_required
def view_requests(request):
    user = request.user
    friends = Friend.objects.requests(user)
    return render(request, 'friends/requests.html', {'friends': friends})

@login_required
def accept_friends(request, friendship_request_id):
    if request.method == 'POST':
        f_request = get_object_or_404(request.user.friend_requests_received,
            id=friendship_request_id)

        f_request.accept()

    return redirect('friends:view_requests')

@login_required
def cancel_friends(request, friendship_request_id):
    if request.method == 'POST':
        f_request = get_object_or_404(request.user.friend_requests_sent,
            id=friendship_request_id)

        f_request.cancel()

    return redirect('friends:view_requests')

@login_required
def reject_friends(request, friendship_request_id):
    if request.method == 'POST':
        f_request = get_object_or_404(request.user.friend_requests_received,
            id=friendship_request_id)

        f_request.decline()

    return redirect('friends:view_requests')

@login_required
def add_friends(request, to_username):
    if request.method == 'POST':
        to_user = get_object_or_404(Account, username=to_username)
        from_user = request.user

        content = {"user": to_user}

        try:
            Friend.objects.add_friend(from_user, to_user)
        except Exception as e:
            content['errors'] = ["%s" %(e)]
        else:
            return redirect('friends:view_requests')

    return render(request, 'user_profiles/user_profile.html', content)

@login_required
def remove_friend(request, friend_username):
    if request.method == 'POST':
        to_user = get_object_or_404(Account, username=friend_username)
        from_user = request.user
        Friend.objects.remove_friend(from_user, to_user)

    return redirect('friends:view_friends')
