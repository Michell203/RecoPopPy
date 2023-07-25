from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User, auth
from django.contrib import messages
from src.models import Profile, Collection, Post, LikePost, FollowersCount
from django.contrib.auth.decorators import login_required
from .main import get_trackID

# Create your views here.

# def index(response):
#     return render(response, "home.html")

@login_required(login_url='login')
def home(response):
    # user_object = User.objects.get(username = response.username)
    # user_profile = Profile.objects.get(user=user_object)
    user_profile = Profile.objects.get(user=response.user)

    posts = Post.objects.all()

    return render(response, "home.html", {'user_profile':user_profile, 'posts':posts})

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

@login_required(login_url='login')
def upload(response):

    if response.method == 'POST':
        user = response.user.username
        track = response.POST['track_name']
        track_id = get_trackID(trackName=track)
        caption = response.POST['caption']
        user_profile = Profile.objects.get(user=response.user)


        new_post = Post.objects.create(user=user, track_name=track, track_id=track_id, caption=caption, user_profile=user_profile)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='login')
def like_post(response):
    username = response.user.username
    post_id = response.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes += 1
        post.save()
        return redirect('/')
    
    else:
        like_filter.delete()
        post.no_of_likes -= 1
        post.save()
        return redirect('/')

@login_required(login_url='login')
def profile(response, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
    }

    return render(response, 'profile.html', context)

@login_required(login_url='login')
def follow(response):
    if response.method == 'POST':
        follower = response.POST['follower']
        user = response.POST['user']
        print(follower)
        print(user)
        print("here")

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('profile/'+user)
        
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('profile/' + user)

    else:
        print("here1")
        return redirect('/')    

