from django.shortcuts import render, redirect
from django.http import HttpResponse
from.models import User, Topic, Subtopic, Matching, Point, Question, Answer

def home(request):
    topics = Topic.objects.all()
    context = {'topics':topics}
    return render(request, 'base/home.html', context)
