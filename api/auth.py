from rest_framework.authentication import SessionAuthentication
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class CsrfExemptSessionAuthentication(SessionAuthentication):

    # To not perform the csrf check previously happening
    def enforce_csrf(self, request):
        return


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


