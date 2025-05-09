from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def crear_token_autenticacion(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
