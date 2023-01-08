from django.db import models

# Create your models here.
class AuthTokens(models.Model):
    user = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    access_token = models.CharField(max_length=150)
    refresh_token = models.CharField(max_length=150)
    token_type = models.CharField(max_length=50)
    expires_at = models.DateTimeField()

class CodeVerifier(models.Model):
    user = models.CharField(max_length=50)
    code_verifier = models.CharField(max_length = 128)