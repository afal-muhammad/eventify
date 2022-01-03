import datetime
import json
import os
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from applications.accounts.models import User
from applications.events.models import Events

# Create your views here.
class LoginView(View):

    def get(self, request, *args, **kwargs):
        return render(self.request, 'login.html')

    def post(self,request):
        username = self.request.POST['username']
        password = self.request.POST['password']
        if username and password:
            user = authenticate(username=username, password=password)
        else:
            data = {}
            data['result'] = "please fill both fields"
            return HttpResponse(json.dumps(data),content_type="application/json")
        if user:
            login(self.request, user)
            data = {}
            data['result'] = "success"
            return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            data ={}
            data['result'] = "invalid credentials"
            return HttpResponse(json.dumps(data),content_type="application/json")


class SignUpView(View):

    def get(self, request, *args, **kwargs):
        return render(self.request, 'signup.html')

    def post(self,request):
        if self.request.POST['first_name'] and self.request.POST['last_name'] and \
                self.request.POST['password']:
            user = User()
            user.first_name = self.request.POST['first_name']
            user.last_name = self.request.POST['last_name']
            user.email = user.username = self.request.POST['email']
            user.set_password(self.request.POST['password'])
            emails = list(User.objects.values_list("email", flat=True))
            if not user.username in emails:
                user.save()
                data = {}
                data['result'] = "success"
                login(self.request,user)
                return HttpResponse(json.dumps(data),
                                    content_type="application/json")
            else:
                data = {}
                data['result'] = "User already exist.Please login"
                return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            data = {}
            data['result'] = "All fields are mandatory"
            return HttpResponse(json.dumps(data),
                                content_type="application/json")



class LogoutView(View):

    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('/login')


class LandingView(View):

    def get(self, *args, **kwargs):
        # events = Events.objects.filter(is_published=True, start_date__gte=datetime.datetime.now() + \
        #                                                               datetime.timedelta(hours=1)).order_by("start_date")
        events = Events.objects.filter(is_published=True, start_date__gt=datetime.datetime.now()).order_by('start_date')
        return render(self.request, 'landing.html',{"events":events})


class MyeventsView(View):

    def get(self, *args, **kwargs):
        events = Events.objects.filter(user_obj=self.request.user).order_by("start_date")
        return render(self.request, 'event-listing.html',{"events":events})