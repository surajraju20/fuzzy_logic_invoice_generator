from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from invoice.models import College, Trainer


def home(request):
    # return HttpResponse("Hello world")
    return render(request, 'home.html')


def show(request):
    colleges = College.objects.all()
    return render(request, "show.html", {'colleges': colleges})


def index(request):
    colleges = College.objects.all()
    trainers = Trainer.objects.all()
    return render(request, "suraj.html", {'colleges': colleges, 'trainers': trainers})


