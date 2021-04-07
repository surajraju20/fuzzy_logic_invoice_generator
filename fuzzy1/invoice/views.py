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

        data_table = [[request.POST['date0'], college_name, int(request.POST['fees0']), int(request.POST['travel0']), int(request.POST['food0'])]]

        number_of_rows = int(request.POST['count'])
        for i in range(1, no_days+1):
            data_table.append([request.POST['date'+str(i)], college_name, int(request.POST['fees'+str(i)]), int(request.POST['travel'+str(i)]), int(request.POST['food'+str(i)])])

        email_generator(trainer_name, remuneration, college_name, acc_no,
                        ifsc, pan, phone, email, location,
                        start_date, end_date, data_table)

        return HttpResponse("Invoice has been sent to your email")

    else:
        print("got get")
        return render(request, "invoice.html")


def email_generator(trainer_name, remuneration, college_name, acc_no,
                    ifsc, pan, phone, email, location, start_date,
                    end_date, data_table):
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

    pdf_generator(trainer_name, acc_no,
                  ifsc, pan, phone, email, location, data_table)

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


def pdf_generator(name1, dbacno, dbifsc, dbpan, dbphno, dbemail, dbloc, data_table):
    print(data_table)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 20)
    pdf.cell(200, 10, 'Genesis Invoice Generation', ln=1, align='C')
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, 'Name (As per bank account): ' + str(name1), ln=4)
    pdf.cell(40, 10, 'Bank account number: ' + str(dbacno), ln=5)
    pdf.cell(40, 10, 'IFSC Code: ' + str(dbifsc), ln=6)
    pdf.cell(40, 10, 'Pan Number: ' + str(dbpan), ln=7)
    pdf.cell(40, 10, 'Phone Number: ' + str(dbphno), ln=8)
    pdf.cell(40, 10, 'Email Id: ' + str(dbemail), ln=9)
    pdf.cell(40, 10, 'Base Location : ' + str(dbloc), ln=10)
    pdf.cell(40, 10, '', ln=11)

    spacing = 1
    data_table.insert(0, ['Date', 'College', 'Fees/day', 'Travel Allowance', 'Food Allowance'])

    col_width = pdf.w / 5.7
    row_height = pdf.font_size * 1.8
    for row in data_table:
        for item in row:
            pdf.cell(col_width, row_height * spacing, txt=str(item), border=1, align="C")
        pdf.ln(row_height * spacing)

    ren = 0
    travel = 0
    food = 0
    for i in data_table[1:]:
        ren += i[2]
        travel += i[3]
        food += i[4]
    grand = ren + travel + food

    pdf.cell(col_width * 2, row_height * spacing, txt="Total", border=1, align="C")
    pdf.cell(col_width, row_height * spacing, txt=str(ren), border=1, align="C")
    pdf.cell(col_width, row_height * spacing, txt=str(travel), border=1, align="C")
    pdf.cell(col_width, row_height * spacing, txt=str(food), border=1, align="C")
    pdf.ln(row_height * spacing)
    pdf.cell(col_width * 4, row_height * spacing, txt="Grand Total", border=1, align="C")
    pdf.cell(col_width, row_height * spacing, txt=str(int(grand)), border=1, align="C")
    pdf.ln(row_height * spacing)
    pdf.cell(col_width * 5, row_height * spacing, txt="Rupees: " + str(int(grand)), border=1, align="C")

    pdf.output("invoice/Invoice.pdf")
