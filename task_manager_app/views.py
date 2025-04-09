from django.http import HttpResponse
from django.shortcuts import render

def user_hallo(request):
    return HttpResponse("Hello, World")


