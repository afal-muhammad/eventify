from django.urls import path
from applications.accounts import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    # path('404/', views.handler404, name="handeler-404"),
    # path('500/', views.handler500, name="handeler-500"),
    path('my-events/', views.MyEventsView.as_view(), name="my-events"),
    ]
handler404 = views.handler404
handler500 = views.handler500