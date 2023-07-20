from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User, auth
from django.contrib import messages
from src.models import Profile, Collection
from django.contrib.auth.decorators import login_required

# Create your views here.

# def index(response):
#     return render(response, "home.html")

@login_required(login_url='login')
def home(response):
    return render(response, "home.html")

def signup(response):

    if response.method == 'POST':
        username = response.POST['username']
        email = response.POST['email']
        password = response.POST['password']
        password2 = response.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(response, 'Email Taken')
                return redirect('signup')
            
            elif User.objects.filter(username=username).exists():
                messages.info(response, 'Username Taken')
                return redirect('signup')
            
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #Log user in and direct to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(response, user_login)

                #Create a profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(response, 'Passwords do not match')
            return redirect('signup')

    else:
        return render(response, "signup.html")

def login(response):

    if response.method == 'POST':
        username = response.POST['username']
        password = response.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(response, user)
            return redirect('/')
        else:
            messages.info(response, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(response, "login.html")

@login_required(login_url='login')
def logout(response):
    auth.logout(response)
    return redirect('login')

@login_required(login_url='login')
def settings(response):
    user_profile = Profile.objects.get(user=response.user)

    if response.method == 'POST':

        if response.FILES.get('image') == None: # No image being sent
            image = user_profile.profileimg
            bio = response.POST['bio']
            location = response.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location

            user_profile.save()

        if  response.FILES.get('image') != None:
            image = response.FILES.get('image')
            bio = response.POST['bio']
            location = response.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location

            user_profile.save()

        return redirect('settings')    


    return render(response, "settings.html", {'user_profile': user_profile}) 