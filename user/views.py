from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.urls import reverse
from django.utils.translation import get_language, gettext_lazy as _
from .user_crypt import decoder
from .tasks import mail_send
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm

User = get_user_model()

class PasswordReset(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data['email']
        if not User.objects.filter(email__iexact=email).exists():
            messages.error(self.request, _(f"No user with email {email} exists."))
            return render(self.request, 'registration/password_reset_form.html')


        self.extra_email_context = {
            'fullurlstatic': self.request.build_absolute_uri('/static/'),
            'host': self.request.get_host(),
            'protocol': self.request.scheme,
        }
        self.html_email_template_name = 'email/password_reset_email.html'
        self.email_template_name = 'email/password_reset_email.txt'

        return super().form_valid(form)


def activate_user_account(request, signed_user=None):
    user, signature = decoder(request, signed_user)
    if user and signature:
        user.email_confirmed = True
        user.save()
        return render(request, 'email_verify_done.html', {'user': user})

    elif user:
        host = request.get_host()
        scheme = request.scheme
        lang = get_language()
        mail_send.delay(lang, scheme, host, user.pk)
        return render(request, 'email_verify_end_of_time.html')

    else:
        return render(request, 'user_does_not_exist.html')


def signup(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            mail_send.delay(get_language(), request.scheme, request.get_host(), new_user.pk)
            return render(request, 'registration/signup_done.html', {'new_user': new_user})

    else:
        user_form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'user_form': user_form})



class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        auth_login(self.request, form.get_user(), backend='users.authentication.CustomModelBackend')
        return HttpResponseRedirect(self.get_success_url())


    def form_invalid(self, form):
        num_attempt = self.request.session.get('num_attempt', 0)
        if num_attempt < 2:
            self.request.session['num_attempt'] = num_attempt + 1
        
        else:
            self.request.session['num_attempt'] = 2


        context = self.get_context_data(form=form)
        context['num_attempt'] = num_attempt

        # if num_attempt == 1:
        #     post_url = self.request.scheme + '://' + self.request.get_host() + reverse('v2:reset_password_reset')
        #     post_data = {'email': self.request.POST['username']}
        #     reset_pass_email(post_url, post_data)

        return self.render_to_response(context=context)