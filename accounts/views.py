from django.http import HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from accounts.forms import UserCreationForm
from accounts.login_required import LoginRequiredMixin


class SignUpView(FormView):
    form_class = UserCreationForm
    success_url = reverse_lazy(
        'tweet_overview:index', kwargs={
            'category': 'politics'})
    template_name = 'registration/signup.html'

    def get_success_url(self, user=None):
        return super().get_success_url()

    def form_valid(self, form):
        return HttpResponseRedirect(self.get_success_url(self.register(form)))

    def register(self, form):
        new_user = form.save()
        return new_user


class MyProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile/my_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.name
        return context
