from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from invoice.models import College, Trainer


def index(request):
    colleges = College.objects.all()
    trainers = Trainer.objects.all()
    return render(request, "suraj.html", {'colleges': colleges, 'trainers': trainers})


def generate(request):
    print("got in generate")
    if request.method == 'POST':
        print("got post")
        trainer_name = request.POST['trainer_name']
        print(trainer_name)
        email = Trainer.objects.all().filter(t_name=trainer_name)[0].email_id
        email_generator(request,
                        request.POST['start_date'],
                        request.POST['end_date'],
                        request.POST['college_name'],
                        email)
        return HttpResponse("Invoice has been sent to your email")

    else:
        print("got get")
        return HttpResponse("no get request allowed")


def email_generator(request, start, end, college, email):
    # set up the SMTP server
    s = SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login("namanprakash5@gmail.com", "eipw cimf lcix lrzz")
    msg = MIMEMultipart()  # create a message
    # add in the actual person name to the message template

    message = "Hello This is a text message " + start + " to " + end
    # setup the parameters of the message
    msg['From'] = "namanprakash5@gmail.com"
    msg['To'] = email
    msg['Subject'] = "Training at " + college
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    # send the message via the server set up earlier.
    s.send_message(msg)
    del msg
