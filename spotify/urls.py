from django.contrib import admin
from django.urls import path, include
from .views import *
from .utils import refresh_user_tokens

urlpatterns = [
    path('redirect', spotify_callback),
    path('check-auth', CheckAuthenticated.as_view()),
    path('get-auth-url', GetAuthUrl.as_view()),
    path('clear-all', ClearAll.as_view()),
    path('all-auth', AuthView.as_view()),
    path('current-song', CurrentSong.as_view()),
    path('search-songs', SearchSongs.as_view()),
    path('queue', QueueSong.as_view()),
    path('clean-queue', CleanQueue.as_view()),
    path('refresh', refresh_user_tokens),
]