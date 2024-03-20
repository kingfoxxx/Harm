from django.urls import path
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import CustomUser
from .forms import SignUpForm
from dotenv import load_dotenv
import os
import json
import base64
from requests import post, get
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def get_token():
    client_id="34feb190cc0f4876b1b962313ac49396"
    client_secret="70449f31f55c434b914f078fae8d5a4a"
    auth_string=client_id + ":" + client_secret
    auth_bytes=auth_string.encode("utf-8")
    auth_base64=str(base64.b64encode(auth_bytes), "utf-8")
    url="https://accounts.spotify.com/api/token"
    headers={
        "Authorization":"Basic " + auth_base64,
        "Content-Type":"application/x-www-form-urlencoded"
    }
    data={"grant_type": "client_credentials"}
    result=post(url, headers=headers, data=data)
    json_result=json.loads(result.content)
    token=json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token} 

@login_required(login_url='login')
def home(request):
    return render(request,'Harmony/home.html')


def loginuser(request):
    if request.method == "POST":
        username_or_email = request.POST.get('email')  # Use get to avoid KeyError if key is not present
        password = request.POST.get('password')
        user = authenticate(request, username=username_or_email, password=password)
        if user is not None:
            # Authentication successful, log in the user
            login(request, user)
            return redirect('home-page')  # Redirect to a success page
        else:
            # Authentication failed, handle the error (e.g., show an error message)
            return render(request, 'Harmony/login.html', {'error_message': 'Invalid username or password'})
        return HttpResponse(password)  
    else:
        return render(request,'Harmony/login.html')
    

def signup(request):
    if request.method == "post":  # Change "post" to "post"
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return render(request, 'Harmony/login.html')
    else:
        return render(request, 'Harmony/signup.html')


@login_required(login_url='login')
def myartists(request):
    return render(request,'Harmony/artists.html')

@login_required(login_url='login')
# @csrf_exempt
def search(request):
    if 'q' in request.GET:
        term=request.GET["q"]
        token=get_token()
        headers=get_auth_header(token)
        url=f'https://api.spotify.com/v1/search?q={term}&type=track%2Cartist'
        result=get(url, headers=headers)
        json_result=json.loads(result.content)
        return term
    else:
        return render(request,'Harmony/search.html')

@login_required
def my_protected_view(request):
    # Your protected view logic here
    pass


def landing_page(request):
    return render(request, 'Harmony/index.html')


# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')  # Redirect to your home page
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'Harmony/register.html', {'form': form})
