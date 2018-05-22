from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. Your at the polls index")

def detail(request, question_id):
    return HttpResponse("(detail)You're looking at question %s." % question_id)

def results(request, question_id):
    response = "(results)You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("(vote)You're voting on question %s." % question_id)
    