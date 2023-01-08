from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from requests import Request, post
from .utils import *
from .credentials import CLIENT_ID, REDIRECT_URI, PKCE
from .models import AuthTokens
from .serializers import AuthTokensSerializer
from api.models import Playback, User, Song, Queue

# Create your views here.
class ClearAll(APIView):
    def get(self,request, format=None):
        AuthTokens.objects.all().delete()
        CodeVerifier.objects.all().delete()
        return Response({'all gone' : 'ya'}, status=status.HTTP_200_OK)

class AuthView(generics.ListAPIView):
    queryset = AuthTokens.objects.all()
    serializer_class = AuthTokensSerializer


class GetAuthUrl(APIView):
    def get(self,request, format=None):
        client_id = CLIENT_ID
        response_type = 'code'
        redirect_uri = REDIRECT_URI
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'
        code_challenge_method = 'S256'
        user = request.session.session_key
        code_verifier = get_code_verifier(user)
        code_challenge = generate_code_challenge(code_verifier)
        if PKCE:
            url = Request('GET', 'https://accounts.spotify.com/authorize', params={
                'response_type': response_type,
                'redirect_uri': redirect_uri,
                'client_id': client_id,
                'scope' : scopes,
                'code_challenge_method' : code_challenge_method,
                'code_challenge' : code_challenge}).prepare().url
        else:
            url = Request('GET', 'https://accounts.spotify.com/authorize', params={
                'response_type': response_type,
                'redirect_uri': redirect_uri,
                'client_id': client_id,
                'scope' : scopes}).prepare().url
        

        return Response({'url': url}, status=status.HTTP_200_OK)

def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')
    client_id = CLIENT_ID
    redirect_uri = REDIRECT_URI
    user = request.session.session_key
    code_verifier = get_code_verifier(user)
    if PKCE:
        response = post('https://accounts.spotify.com/api/token', data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'code_verifier': code_verifier,
        }).json()
    else:
        response = post('https://accounts.spotify.com/api/token', data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri
        }).json()
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    expires_at = get_expires_at(expires_in)
    error = response.get('error')

    if not request.session.exists(request.session.session_key):
        request.session.create()

    user = request.session.session_key

    update_or_create_user_tokens(
            user = user, 
            access_token = access_token, 
            token_type = token_type, 
            expires_at = expires_at, 
            refresh_token = refresh_token
        )

    return redirect('frontend:party')

class CheckAuthenticated(APIView):
    def get(self,request, format=None):
        if not request.session.exists(request.session.session_key):
            request.session.create()
        user = request.session.session_key
        is_authenticated = is_user_authenticated(user)
        return Response({'is_authenticated': is_authenticated}, status=status.HTTP_200_OK)

class CurrentSong(APIView):
    def delete_other_instances(self,song_tag, party):
        Song.objects.filter(tag=song_tag, party=party).delete()
    
    def get(self, request, format=None):
        host = request.session.session_key
        user = User.objects.filter(user=host, is_host=True)[0]
        party_code = user.party_code
        playback = Playback.objects.filter(party_code=party_code)[0]
        party = Party.objects.filter(code=party_code)[0]
        endpoint = "me/player/currently-playing"
        params = {}
        response = execute_spotify_api_request(host, endpoint, params)

        if 'error' in response or 'item' not in response:
            playback.song_tag = None
            playback.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            item = response.get('item')
            song = get_song(
                item, 
                progress=response.get('progress_ms'), 
                is_playing=response.get('is_playing')
            )
            if(playback.song_tag == song.get('id')):
                song_found = Song.objects.filter(tag=playback.song_tag, party = party.id)
                if(song_found):
                    song_model = song_found[0]
                    song_model.time = song.get('time')
                    song_model.is_playing = song.get('is_playing')
                    song_model.save()
            else:
                queue_model = Queue.objects.filter(song_tag=song.get('id'), party_code=party_code)
                if queue_model:
                    username = queue_model[0].username
                else:
                    username = ""

                new_song_model = Song(
                    title = song.get('title'),
                    artist = song.get('artist'),
                    duration = song.get('duration'),
                    time = song.get('time'),
                    album_cover = song.get('album_cover'),
                    is_playing = song.get('is_playing'),
                    tag = song.get('id'),
                    party=party,
                    username=username
                )
                self.delete_other_instances(new_song_model.tag, party)
                new_song_model.save()
                playback.song_tag = new_song_model.tag
                playback.fire = 0
                playback.username = username
                playback.save()
                users_in_party = User.objects.filter(party_code=party_code)
                for user in users_in_party:
                    if user.gave_fire:
                        user.gave_fire = False
                        user.save()

            return Response(song, status=status.HTTP_200_OK)

class SearchSongs(APIView):
    lookup_url_kwarg = 'query'
    def get(self, request, format=None):
        user = request.session.session_key
        host = get_host(user)
        if host == None:
            return Response({'ERR': 'Could not find host'}, status=status.HTTP_400_BAD_REQUEST)
        query = request.GET.get(self.lookup_url_kwarg)
        endpoint = "search"
        params = {
            'q': query,
            'type': 'track',
            'limit': '20',
        }
        response = execute_spotify_api_request(host, endpoint, params)
        items = response.get('tracks').get('items')
        songs = []
        for item in items:
            song = get_song(item)
            songs.append(song)

        if 'error' in response:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(songs, status=status.HTTP_200_OK)

class QueueSong(APIView):
    lookup_url_kwarg = 'song_id'
    def post(self, request, format=None):
        user = request.session.session_key
        host = get_host(user)
        if host == None:
            return Response({'ERR': 'Could not find host'}, status=status.HTTP_400_BAD_REQUEST)
        song_id = request.data.get(self.lookup_url_kwarg)
        uri = 'spotify:track:' + song_id

        endpoint = "me/player/queue"
        params = {
            'uri' : uri
        }

        response = execute_spotify_api_request(host, endpoint, params, post_=True)
        host_model = User.objects.filter(user=host)[0]
        user_model = User.objects.filter(user=user)[0]
        model = Queue(
            party = host_model.party,
            party_code = host_model.party_code,
            song_tag = song_id,
            user = user,
            username = user_model.username
        )
        model.save()
        return Response({'Success':'added to queue'}, status.HTTP_204_NO_CONTENT)

class CleanQueue(APIView):
    def post(self, request, format=None):
        user = request.session.session_key
        host = get_host(user)
        if host == None:
            return Response({'ERR': 'Could not find host'}, status=status.HTTP_400_BAD_REQUEST)

        endpoint = "me/player/queue"
        params = {}
        response = execute_spotify_api_request(host, endpoint, params)
        song_ids = []
        if response.get("currently_playing") != None:
            song_ids.append(response.get("currently_playing").get('id'))
        in_queue = response.get("queue")
        for item in in_queue:
            id = item.get('id')
            song_ids.append(id)

        host_model = User.objects.filter(user=host)[0]
        party_code = host_model.party_code
        room_queues = Queue.objects.filter(party_code=party_code)
        for queue in room_queues:
            song_tag = queue.song_tag
            if(song_tag not in song_ids):
                queue.delete()
        return Response({'success': 'cleaned queue'}, status.HTTP_200_OK) 