from __future__ import absolute_import, unicode_literals
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from .user_crypt import encoder
from django.utils import translation



User = get_user_model()


def mail_send(lang, scheme, host, user_id, app_name="SyTech"):
    user = User.objects.filter(pk=user_id).first()
    text_content = "Account activation"
    subject = "Email confirmation"
    template_name = "email/activation.html"
    from_email = settings.EMAIL_HOST_USER
    recipients = [user.email]

    translation.activate(lang)
    context = encoder(scheme, host, user, app_name)
    html_content = render_to_string(template_name, context)
    html_content = translation.gettext(html_content)

    email = EmailMultiAlternatives(subject, text_content, from_email, recipients)
    email.attach_alternative(html_content, "text/html")
    mail_sent = email.send()

    return mail_sent
