'''logic for user model'''
from django.contrib.auth import get_user_model
from django.http import Http404

def get_deleted_stand_in_user():
    '''creates and adds deleted user profile'''
    return get_user_model().objects.get_or_create(username='deleted-user')[0]

def check_user(request, obj):
    if request.user != obj.user:
        raise Http404