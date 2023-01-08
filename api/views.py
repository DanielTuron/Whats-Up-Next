from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from spotify.views import CurrentSong

# Create your views here.
class HelloWorld(APIView):
    serializer_class = HelloWorldSerializer
    Party.objects.all().delete()
    User.objects.all().delete()
    def get(self,request, format=None):
        model = HelloWorldModel()
        serializer = self.serializer_class(model)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PartiesView(generics.ListAPIView):
    queryset = Party.objects.all()
    serializer_class = PartySerializer

class CreateParty(APIView):
    def deleteOtherInstances(self,host):
        Party.objects.filter(host=host).delete()
        
    serializer_class = CreatePartySerializer
    def post(self, request, format=None):
        if not request.session.exists(request.session.session_key):
            request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            max_queues = serializer.data.get('max_queues')
            host = self.request.session.session_key
            self.deleteOtherInstances(host)
            model = Party(
                host = host,
                max_queues = max_queues,
            )
            serializer = PartySerializer(model)
            model.save()
            playback = Playback(
                party = model,
                party_code = model.code,
            )
            playback.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class UsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AddUser(APIView):
    def deleteOtherInstances(self,user):
        User.objects.filter(user=user).delete()

    serializer_class = AddUserSerializer
    def post(self, request, format=None):
        if not request.session.exists(request.session.session_key):
            request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get('username')
            is_host = serializer.data.get('is_host')
            party_code = serializer.data.get('party_code')
            party_found = Party.objects.filter(code=party_code)
            if party_found:
                party = party_found[0]
                user = self.request.session.session_key
                self.deleteOtherInstances(user)
                model = User(
                    user = user,
                    username = username,
                    is_host = is_host,
                    party = party,
                    party_code = party_code,
                )
                serializer = UserSerializer(model)
                model.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'Not found': 'No party matching code...'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class UserParty(APIView):
    serializer_class = PartySerializer

    def get(self,request, format=None):
        user = self.request.session.session_key
        this_user = User.objects.filter(user=user)
        if this_user:
            party = this_user[0].party
            data = PartySerializer(party).data
            data['is_host'] = self.request.session.session_key == party.host
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'Not Found': 'No party containing user...'}, status=status.HTTP_404_NOT_FOUND)  

class GetParty(APIView):
    serializer_class = PartySerializer
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):
        party_code = request.GET.get(self.lookup_url_kwarg)
        if party_code != None:
            party_found = Party.objects.filter(code=party_code)
            if party_found:
                party = party_found[0]
                serializer = PartySerializer(party)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'Not found': 'No party matching code...'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class LeaveParty(APIView):
    def post(self, request, format=None):
        user_key = self.request.session.session_key
        this_user = User.objects.filter(user=user_key)
        if this_user:
            user = this_user[0]
            is_host = user.is_host
            if is_host:
                party = user.party
                party_id = party.id
                Party.objects.filter(id=party_id).delete()
            else:
                user_id = user.id
                User.objects.filter(id=user_id).delete()
            return Response({'Success': 'user deleted'}, status=status.HTTP_200_OK)

        else:
            return Response({'Not found': 'No user found...'}, status=status.HTTP_404_NOT_FOUND)

class TakenUsername(APIView):
    serializer_class = UserSerializer
    lookup_url_kwarg_code = 'code'
    lookup_url_kwarg_username = 'username'

    def get(self, request, format=None):
        party_code = request.GET.get(self.lookup_url_kwarg_code)
        username = request.GET.get(self.lookup_url_kwarg_username)
        if party_code != None and username != None:
            user_found = User.objects.filter(party_code=party_code, username=username)
            if user_found:
                user = user_found[0]
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_302_FOUND)
            else:
                return Response({'No match': 'Username is available'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class CurrentSong(APIView):
    serializer_class = SongSerializer
    def get(self, request, format=None):
        user_key = self.request.session.session_key
        this_user = User.objects.filter(user=user_key)
        if this_user:
            user = this_user[0]
            playback_found = Playback.objects.filter(party_code = user.party_code)
            if playback_found:
                playback = playback_found[0]
                song_found = Song.objects.filter(tag = playback.song_tag)
                if song_found:
                    song = song_found[0]
                    serializer = SongSerializer(song)
                    data = serializer.data
                    data['fire'] = playback.fire
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response({'Not found': 'No song found...'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'Not found': 'No party found...'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'Not found': 'No user found...'}, status=status.HTTP_404_NOT_FOUND)

class GetUserQueues(APIView):
    def get(self, request, format=None):
        user_key = self.request.session.session_key
        num_queues = Queue.objects.filter(user = user_key).count()
        return Response({'num_queues' : num_queues}, status=status.HTTP_200_OK)

class QueuesView(generics.ListAPIView):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer

class GiveFire(APIView):
    def post(self, request, format=None):
        user_key = self.request.session.session_key
        user = User.objects.filter(user=user_key)[0]
        if user.gave_fire:
            return Response({'Not able': 'Already gave fire'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            username = user.username
            playback = Playback.objects.filter(party_code = user.party_code)[0]
            if playback.username == username:
                return Response({'Not able': 'Cannot give fire to own song'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            else:
                playback_user_found = User.objects.filter(username=playback.username)
                if playback_user_found:
                    playback_user = playback_user_found[0]
                    playback_user.fire = playback_user.fire + 1
                    playback_user.save()
                playback.fire = playback.fire + 1
                playback.save()
                user.gave_fire = True
                user.save()
                return Response({'success': 'fire given'}, status=status.HTTP_200_OK)

class IsQueued(APIView):
    lookup_url_kwarg = 'song-id'
    def get(self, request, format=None):
        user_key = self.request.session.session_key
        user = User.objects.filter(user=user_key)[0]
        party = user.party
        song_id = request.GET.get(self.lookup_url_kwarg)
        queue_found = Queue.objects.filter(party=party, song_tag=song_id)
        playback = Playback.objects.filter(party=party)[0]
        queue_exists = False
        if queue_found or playback.song_tag == song_id:
            queue_exists = True
        return Response({'queue_found': queue_exists}, status=status.HTTP_200_OK)

class GetTopDJ(APIView):
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):
        party_code = request.GET.get(self.lookup_url_kwarg)
        if party_code != None:
            party_users = User.objects.filter(party_code=party_code)
            top_dj = party_users.order_by('-fire').first()
            username = top_dj.username
            fire = top_dj.fire
            return Response({'username': username, 'fire': fire}, status=status.HTTP_200_OK)
        else:
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)




