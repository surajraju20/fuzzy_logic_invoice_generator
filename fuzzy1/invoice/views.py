from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from smtplib import SMTP
from fpdf import FPDF
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime, timedelta
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
        college_name = request.POST['college_name']
        remuneration = request.POST['fees0']
        acc_no = Trainer.objects.all().filter(t_name=trainer_name)[0].acc_no
        pan = Trainer.objects.all().filter(t_name=trainer_name)[0].pan
        ifsc = Trainer.objects.all().filter(t_name=trainer_name)[0].ifsc
        phone = Trainer.objects.all().filter(t_name=trainer_name)[0].phone_number
        email = Trainer.objects.all().filter(t_name=trainer_name)[0].email_id
        location = Trainer.objects.all().filter(t_name=trainer_name)[0].t_location
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        edate = datetime.strptime(end_date, '%Y-%m-%d')
        sdate = datetime.strptime(start_date, '%Y-%m-%d')
        no = edate - sdate
        no_days = no.days
        travel = int(request.POST['travel0'])
        food = int(request.POST['food0'])

        email_generator(request, trainer_name, remuneration, college_name, acc_no,
                        ifsc, pan, phone, email, location, no_days, sdate, edate,
                        start_date, end_date, travel, food)

        return HttpResponse("Invoice has been sent to your email")

    else:
        print("got get")
        return HttpResponse("no get request allowed")


def email_generator(request, trainer_name, remuneration, college_name, acc_no,
                    ifsc, pan, phone, email, location, no_days, sdate, edate, start_date,
                    end_date, travel, food):
    # set up the SMTP server
    s = SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login("namanprakash5@gmail.com", "eipw cimf lcix lrzz")
    msg = MIMEMultipart()  # create a message
    # add in the actual person name to the message template

    message = "Greetings from Genesis!!\n" \
              "This is an email confirmation post of our telephonic conversation about associating with Genesis" \
              "of our forth coming project on the contractual basis. PFB the details about the project.\n" \
              "\n" \
              "Name of College\t\t:" + college_name + "\n" \
                                                 "Remuneration\t\t  :" + remuneration + "/- per day incl of TDS\n" \
                                                                                        "Date\t\t\t\t   :" + start_date + " to " + end_date

    pdf_generator(request, trainer_name, remuneration, college_name, acc_no,
                  ifsc, pan, phone, email, location, no_days, sdate, edate,
                  start_date, end_date, travel, food)


    msg['From'] = "namanprakash5@gmail.com"
    msg['To'] = email
    msg['Subject'] = "Confirmation on Genesis Training"

    with open('invoice/Invoice.pdf', 'rb') as file:
        attach = MIMEApplication(file.read(), _subtype='pdf')
    attach.add_header("Content-Disposition", "attachment", filename=str("Invoice.pdf"))
    msg.attach(attach)
    msg.attach(MIMEText(message, 'plain'))

    s.send_message(msg)
    del msg


def pdf_generator(request, name1, remuneration, college, dbacno, dbifsc, dbpan, dbphno, dbemail, dbloc, nodays,
                  sdate, edate, startdate, enddate, Travel, Food):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(200, 10, 'Genesis Invoice Generation', ln=1, align='C')
    pdf.cell(40, 10, 'Name (As per bank account): ' + str(name1), ln=4)
    pdf.cell(40, 10, 'Bank account number: ' + str(dbacno), ln=5)
    pdf.cell(40, 10, 'IFSC Code: ' + str(dbifsc), ln=6)
    pdf.cell(40, 10, 'Pan Number: ' + str(dbpan), ln=7)
    pdf.cell(40, 10, 'Phone Number: ' + str(dbphno), ln=8)
    pdf.cell(40, 10, 'Email Id: ' + str(dbemail), ln=9)
    pdf.cell(40, 10, 'Email Id: ' + str(dbemail), ln=9)
    pdf.cell(40, 10, 'Base Location : ' + str(dbloc), ln=10)
    pdf.cell(40, 10, '', ln=11)

    spacing = 1
    dates = []
    for i in range(nodays):
        s = datetime.strptime(startdate, '%Y-%m-%d')
        s = s + timedelta(i)
        dates.insert(i, str(s.date()))

    data = [['Date', 'College', 'Fees/day', 'Travel Allowance', 'Food Allowance']]
    for j in range(nodays):
        if j == 0 or j == nodays:
            data.insert(j + 1, [dates[j], college, remuneration, str(Travel), str(Food)])
        else:
            data.insert(j + 1, [dates[j], college, remuneration, '0', str(Food)])

    col_width = pdf.w / 5.6
    row_height = pdf.font_size * 2
    for row in data:
        for item in row:
            pdf.cell(col_width, row_height * spacing, txt=item, border=1, align="C")
        pdf.ln(row_height * spacing)

    Ren = int(remuneration) * int(nodays)
    Travel = int(Travel) * 2
    Food = int(Food) * int(nodays)
    Grand = int(Ren) + int(Travel) + int(Food)

    pdf.cell(col_width * 2, row_height * spacing, txt="Total", border=1, align="C")
    pdf.cell(col_width, row_height * spacing, txt=str(int(Ren)), border=1, align="C")
    pdf.cell(col_width, row_height * spacing, txt=str(int(Travel)), border=1, align="C")
    pdf.cell(col_width, row_height * spacing, txt=str(int(Food)), border=1, align="C")
    pdf.ln(row_height * spacing)
    pdf.cell(col_width * 4, row_height * spacing, txt="Grand Total", border=1, align="C")
    pdf.cell(col_width, row_height * spacing, txt=str(int(Grand)), border=1, align="C")
    pdf.ln(row_height * spacing)
    pdf.cell(col_width * 5, row_height * spacing, txt="Rupees: " + str(int(Grand)), border=1, align="C")

    pdf.output("invoice/Invoice.pdf")
