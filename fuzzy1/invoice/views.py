from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

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
    email_generator(request)
    return render(request, "suraj.html", {'colleges': colleges, 'trainers': trainers})

def email_generator(request):
    # set up the SMTP server
    s = SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login("namanprakash5@gmail.com", "eipw cimf lcix lrzz")

    # For each contact, send the email:
    for name, email in [("Aman", "aman30865@gmail.com")]:
        msg = MIMEMultipart()  # create a message
        # add in the actual person name to the message template
        message = "Hello This is a text message"
        # setup the parameters of the message
        msg['From'] = "namanprakash5@gmail.com"
        msg['To'] = email
        msg['Subject'] = "This is TEST"
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
