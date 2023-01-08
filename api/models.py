from django.db import models
import string, random

# Create your models here.
CODE_LEN = 4
#demo
class HelloWorldModel(models.Model):
    msg = models.CharField(max_length=50)
    def __init__(self):
        self.msg = 'hello world'

#generate a unique party code
def generate_code():
    unique = False
    #Join 4 random lower case characters
    while not unique:
        code = ''.join(random.choice(string.ascii_lowercase) for _ in range(CODE_LEN))
        parties_with_code = Party.objects.filter(code=code)
        if not parties_with_code:
            unique = True
    return code

class Party(models.Model):
    code = models.CharField(
        max_length=CODE_LEN, 
        unique=True,
        editable=False,
        default=generate_code,
        )
    host = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    max_queues = models.IntegerField()

class User(models.Model):
    user = models.CharField(max_length=50)
    username = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    is_host = models.BooleanField(default=False)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    party_code = models.CharField(max_length=CODE_LEN)
    fire = models.IntegerField(default=0)
    gave_fire = models.BooleanField(default=False)

class Song(models.Model):
    title = models.TextField()
    artist = models.TextField()
    duration = models.IntegerField()
    album_cover = models.CharField(max_length=200)
    time = models.IntegerField(default=None, null=True)
    is_playing = models.BooleanField(default=False)
    tag = models.CharField(max_length=50)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    username = models.CharField(max_length=20)

class Playback(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    song_tag = models.CharField(max_length=50, default=None, null=True)
    party_code = models.CharField(max_length=CODE_LEN)
    username = models.CharField(max_length=20)
    fire = models.IntegerField(default=0)

class Queue(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    party_code = models.CharField(max_length=CODE_LEN)
    song_tag = models.CharField(max_length=50)
    user = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

