import pandas as pd
import numpy as np
from django.core.mail import EmailMultiAlternatives
from datetime import datetime

from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from django.template.loader import render_to_string

CERTIFICATE_TEMP_SAVEPATH = 'user_certificate.pdf'
OUTPUT_LOG_PATH = 'log.csv'
FROM_EMAIL='30works <info@thirty.works>'
CERTIFICATE_TEMPLATE_PATH = "certificate.pdf"
EMAIL_SUBJECT = 'You completed 30/30'
CSV_FILE = 'test.csv'
YEAR = datetime.now().year


# load list of users and emails to receive certificates
df_user_list = pd.read_csv(CSV_FILE).replace({np.nan: None}) # All blank fields is replaced with None
f = open('log.txt', 'a')

for i, row in df_user_list.iterrows():
    
    first_name, last_name, user_email = row['first_name'], row['last_name'], row['email']
    full_name = f'{first_name} {last_name}' if last_name else f'{first_name}'
    print(full_name)
 
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    # can = canvas.Canvas(packet, pagesize=letter)
    can = canvas.Canvas(packet)
    # can.drawString(50, 100, "Hello !!! !  ! !!! :)")
    can.setFillColor(HexColor('#a87b00'))
    can.setFont("Helvetica", 28)
    can.drawCentredString(x=840/2, y=280, text=full_name)
    can.save()

    #move to the beginning of the StringIO buffers
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open(CERTIFICATE_TEMPLATE_PATH, "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open(CERTIFICATE_TEMP_SAVEPATH, "wb")
    output.write(outputStream)
    outputStream.close()

    alt_message = render_to_string(
        'email/complete_3030.html',
        {
            'user_first_name': first_name,
            'year': YEAR,
        }
    )
    message = render_to_string(
        'email/complete_3030.txt',
        {
            'user_first_name': first_name,
            'year': YEAR,
        }
    )

    # # now create an email message
    email = EmailMultiAlternatives(
        subject=EMAIL_SUBJECT,
        body=message,
        from_email=FROM_EMAIL,
        to=[user_email],
    )
    email.attach_alternative(alt_message, "text/html")
    email.attach_file(CERTIFICATE_TEMP_SAVEPATH)
    email.content_subtype = 'html'
    email.send()
    text = f'{i+1} - Sent email to {first_name} {last_name}: {user_email} [{datetime.now()}] \n'
    f.write(text)
    print(text)
f.write('\n')
f.write('--------------------------------------------------------------------------')
f.write('\n')
f.close()
 