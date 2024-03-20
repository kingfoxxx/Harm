from.import views
from django.urls import path



urlpatterns = [
    path('home', views.home, name='home-page'),
    path('signup', views.signup, name='signup'),
    path('login', views.loginuser, name='login'),
    path('myartists', views.myartists, name='myartists'),
    path('search', views.search, name='search page'),
    path('', views.landing_page, name='landing_page'),
]
