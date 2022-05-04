from django.contrib.auth.backends import ModelBackend


class CustomModelBackend(ModelBackend):
    def user_can_authenticate(self, user):
        can = super(CustomModelBackend, self).user_can_authenticate(user)
        if can:
            return user.email_confirmed

        return can