from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('hello-world', HelloWorld.as_view()),
    path('create-party', CreateParty.as_view()),
    path('parties', PartiesView.as_view()),
    path('add-user', AddUser.as_view()),
    path('users', UsersView.as_view()),
    path('user-party', UserParty.as_view()),
    path('get-party', GetParty.as_view()),
    path('leave-party', LeaveParty.as_view()),
    path('taken-username', TakenUsername.as_view()),
    path('current-song', CurrentSong.as_view()),
    path('get-num-queues', GetUserQueues.as_view()),
    path('queues', QueuesView.as_view()),
    path('give-fire', GiveFire.as_view()),
    path('is-queued', IsQueued.as_view()),
    path('get-top-dj', GetTopDJ.as_view())
]