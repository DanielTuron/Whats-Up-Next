from .models import AuthTokens, CodeVerifier
from django.utils import timezone
from datetime import timedelta
from .credentials import CLIENT_ID
from requests import post, put, get
from api.models import Party, User
import pkce


BASE_URL = "https://api.spotify.com/v1/"

def get_code_verifier(user):
    matches = CodeVerifier.objects.filter(user=user)
    if matches:
        code_verifier = matches[0].code_verifier
    else:
        code_verifier = pkce.generate_code_verifier(length=128)
        model = CodeVerifier(
            user=user,
            code_verifier=code_verifier,
        )
        model.save()
    return code_verifier

def generate_code_challenge(code_verifier):
    code_challenge =  pkce.get_code_challenge(code_verifier)
    return code_challenge

def get_expires_at(expires_in):
    safety_buffer = 60 * 3 #We will look for authentification more often than this
    return timezone.now() + timedelta(seconds=expires_in) - timedelta(seconds=safety_buffer)

def get_user_tokens(user):
    user_tokens_found = AuthTokens.objects.filter(user=user)
    if user_tokens_found:
        return user_tokens_found[0]
    else:
        return None

def update_or_create_user_tokens(user, access_token, token_type, expires_at, refresh_token):
    user_tokens_found = AuthTokens.objects.filter(user=user)
    if user_tokens_found:
        user_tokens = user_tokens_found[0]
        user_tokens.access_token = access_token
        user_tokens.token_type = token_type
        user_tokens.expires_at = expires_at
        user_tokens.refresh_token = refresh_token
        user_tokens.save()
    else:
        user_tokens = AuthTokens(user=user, access_token=access_token, token_type=token_type, expires_at=expires_at, refresh_token=refresh_token)
        user_tokens.save()

def refresh_user_tokens(user):
    user_tokens = get_user_tokens(user)
    if user_tokens != None:
        grant_type = 'refresh_token'
        refresh_token = user_tokens.refresh_token
        client_id = CLIENT_ID
        data = {
            'grant_type': grant_type,
            'refresh_token': refresh_token,
            'client_id' : client_id
        }
        headers = {
            'Content-Type' : 'application/x-www-form-urlencoded'
        }

        response = post(BASE_URL + 'refresh', data=data)
        response = post('https://accounts.spotify.com/api/token', data=data, headers=headers).json()
        if 'error' in response:
            return False
        else:
            access_token = response.get('access_token')
            expires_in = response.get('expires_in')
            expires_at = get_expires_at(expires_in)
            token_type = user_tokens.token_type
            update_or_create_user_tokens(
                user = user, 
                access_token = access_token, 
                token_type = token_type, 
                expires_at = expires_at, 
                refresh_token = refresh_token
            )
            return True

def is_user_authenticated(user):
    user_tokens = get_user_tokens(user)
    if user_tokens != None:
        if timezone.now() > user_tokens.expires_at:
            success = refresh_user_tokens(user)
            if success:
                return True
            else:
                user_tokens.delete()
                return False
        else:
            return True
    else:
        return False

def execute_spotify_api_request(session_id, endpoint, params, post_=False, put_=False):
    tokens = get_user_tokens(session_id)

    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': "Bearer " + tokens.access_token, 
    }

    if post_:
        response = post(BASE_URL + endpoint, params=params, headers=headers)
    elif put_:
        response = put(BASE_URL + endpoint, params=params, headers=headers)
    else:
        response = get(BASE_URL + endpoint, params=params, headers=headers)
    try:
        return response.json()
    except:
        return {'Error': 'Issue with request'}

def get_host(user_key):
    user_found = User.objects.filter(user=user_key)
    if user_found:
        user = user_found[0]
    else:
        return None
    party_found = Party.objects.filter(code=user.party_code)
    if party_found:
        party = party_found[0]
        host = party.host
        return host
    else:
        return None

def get_song(item, progress = 0, is_playing = False):
    title = item.get('name')
    duration = item.get('duration_ms')
    album_cover = item.get('album').get('images')[0].get('url')
    song_id = item.get('id')

    artist_string = ""
    for i, artist in enumerate(item.get('artists')):
        if i > 0:
            artist_string += ", "
        name = artist.get('name')
        artist_string += name
        
    song = {
        'title' : title,
        'artist': artist_string,
        'duration': duration,
        'time': progress,
        'album_cover': album_cover,
        'is_playing': is_playing,
        'id': song_id,
    }
    return song
