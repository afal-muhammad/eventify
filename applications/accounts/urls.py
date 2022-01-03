from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from applications.accounts import views
# from applications.accounts.views import handler500, handler404

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('my-events/', views.MyeventsView.as_view(), name="my-events"),
    path('', views.LandingView.as_view(), name="landing")
    ]