from django.urls import path, re_path, reverse_lazy
from django.contrib.auth import views as auth_views

from .views import activate_user_account, signup, CustomLoginView, PasswordReset

# from users.views import validate_username

app_name = 'users'

urlpatterns = [
    re_path(r'activate/(?P<signed_user>[0-9A-Za-z_\-]+/[A-Za-z0-9_=-]+/[A-Za-z0-9_=-]+)/$',
            activate_user_account, name='activate_user_account'),
    path('signup/', signup, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html',
                                                                   success_url=reverse_lazy('users:password_change_done')),
         name="password_change"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_changed.html'), name='password_change_done'),
    path('password_reset/', PasswordReset.as_view(success_url=reverse_lazy('users:password_reset_done')),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/email_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_confirm.html',
                                                                                success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_confirmed.html'), name='password_reset_complete'),
  

]