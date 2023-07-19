from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

# Create your views here.

def index(response):
    return render(response, "home.html")

def home(response):
    return render(response, "home.html")

def signup(response):
    return render(response, "signup.html")
