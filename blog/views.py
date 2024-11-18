from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogpost
# Create your views here.

def blog(request):
    blogpost = Blogpost.objects.all()
    params = {"myposts":blogpost}
    return render(request,'index1.html',params)

def blogpost(request,id):
    post = Blogpost.objects.filter(post_id = id)[0]
    return render(request,'blogpost.html',{'post':post})