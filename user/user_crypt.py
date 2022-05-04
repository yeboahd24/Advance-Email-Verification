from datetime import timedelta
import imp
from multiprocessing import context
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import  force_text
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.conf import settings
from . import app_settings
from django.urls import reverse

User = get_user_model()
signer = TimestampSigner(sep='/', salt=app_settings.SALT)


def encoder(scheme, host, user, app_name='SyTech'):
    user_crypt = urlsafe_base64_encode(force_bytes(user.id))
    signed_user = signer.sign(user_crypt)
    kwargs = {
        "signed_user": signed_user,
    }

    # Activating url
    activation_url = reverse("users:activate_user_account", kwargs=kwargs)
    activate_url = f"{scheme}://{host}{activation_url}"
    static_url = f"{scheme}://{host}{settings.STATIC_URL}"
    context = {
        "activate_url": activate_url,
        "app_name": app_name,
        "user": user,
        'fullurlstatic': static_url,
    }
    return context



def decoder(request, signed_user):
    try:
        user_encrypt = signer.unsign(signed_user, max_age=timedelta(days=app_settings.CONFIRM_EMAIL_LIFETIME))
        signature = True
    except SignatureExpired:
        user_encrypt = signer.unsign(signed_user, max_age=timedelta(days=365))
        signature = False

    except BadSignature:
        return None, None

    try:
        uid = force_text(urlsafe_base64_decode(user_encrypt))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    return user, signature