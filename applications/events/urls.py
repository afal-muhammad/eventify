from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from applications.events import views
# from applications.accounts.views import handler500, handler404

urlpatterns = [
    path('create-event', views.CreateEventView.as_view(), name="create-event"),
    path('success', views.PaymentSuccessView.as_view(), name="success"),
    path('publish/<slug:slug>/', views.PublishEventView.as_view(), name='publish-event'),
    path('event-detail/<slug:slug>/', views.EventDetailView.as_view(), name='event-detail'),
    path('', views.LandingView.as_view(), name="landing")
    ]