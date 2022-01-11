import datetime
import json
import os
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from applications.accounts.models import User
from applications.events.models import Events

class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.POST.get('next')
        if username and password:
            user = authenticate(username=username, password=password)
        else:
            data = {}
            data['result'] = "please fill both fields"
            return HttpResponse(json.dumps(data),content_type="application/json")
        if user:
            login(self.request, user)
            data = {}
            if next_url:
                data['next'] = next_url
            data['result'] = "success"
            return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            data ={}
            data['result'] = "invalid credentials"
            return HttpResponse(json.dumps(data),content_type="application/json")


class SignUpView(View):

    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request, *args, **kwargs):
        if self.request.POST['email'] and self.request.POST['username'] and \
                self.request.POST['password1'] and self.request.POST["password2"]:
            user = User()
            user.first_name = self.request.POST.get('first_name', None)
            user.last_name = self.request.POST.get('last_name', None)
            user.username = self.request.POST['username']
            user.email = self.request.POST['email']
            try:
                validate_email(user.email)
            except ValidationError as e:
                data = {}
                data['result'] = "Please enter a valid email address"
                return HttpResponse(json.dumps(data),
                                    content_type="application/json")
            if not self.request.POST["password1"] == self.request.POST["password2"]:
                data = {}
                data['result'] = "Both password values should be same"
                return HttpResponse(json.dumps(data),
                                    content_type="application/json")
            user.set_password(self.request.POST['password1'])
            emails_usernames= list(User.objects.values_list("email", "username"))
            lookup_dict = dict(emails_usernames)
            if request.FILES:
                user.image = request.FILES['profile-image']
            if not user.email in lookup_dict.keys() and not user.username in lookup_dict.values():
                user.save()
                data = {}
                data['result'] = "success"
                # login(self.request,user, backend='applications.accounts.backends.EmailModelBackend')
                return HttpResponse(json.dumps(data),
                                    content_type="application/json")
            else:
                data = {}
                data['result'] = "User with same email ID or username already exist.Please login"
                return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            data = {}
            data['result'] = "Fields marked * are mandatory"
            return HttpResponse(json.dumps(data),
                                content_type="application/json")


class LogoutView(View):

    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('/accounts/login')


class MyEventsView(View):

    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        now = datetime.datetime.now()
        events = Events.objects.filter(user_obj=self.request.user).order_by("start_date")
        return render(self.request, 'event-listing.html', {"events": events, 'now': now})


def handler404(request, *args, **argv):
    response = render(request, '404.html')
    return response


def handler500(request, *args, **argv):
    response = render(request, '500.html')
    response.status_code = 500
    return response