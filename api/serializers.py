from rest_framework import serializers
from .models import *

class HelloWorldSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelloWorldModel
        fields = ('msg',)

class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = '__all__'

class GetPartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ('code',)

class CreatePartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ('max_queues',)

class AddUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'party_code', 'is_host',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'    

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'  

class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = '__all__'  


