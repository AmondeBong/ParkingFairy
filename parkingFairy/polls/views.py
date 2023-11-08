from django.http import (HttpResponse, HttpResponseRedirect)
from django.urls import reverse
from django.shortcuts import render


def index(request):
    # return HttpResponse("Hello, world.")
    # return HttpResponseRedirect(reverse('detail', args=[1]))
    return HttpResponseRedirect(reverse('detail', kwargs={'question_id': 1}))


def detail(request, question_id):
    return HttpResponse("You're looking at qustion %s. " % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s"
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s" % question_id)
