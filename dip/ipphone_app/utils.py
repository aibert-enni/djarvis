from django.utils import timezone

from ipphone_app.models import Token


def check_token(token):
    try:
        token = Token.objects.select_related('record').get(token=token)
        if not token or token.expire_time < timezone.now():
            return False

        return token
    except Token.DoesNotExist:
        return False