from django.contrib.auth.mixins import LoginRequiredMixin


class LoginRequiredMixin(LoginRequiredMixin):
    login_url = "/accounts/login"
