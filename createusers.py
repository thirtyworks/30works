"""
Usage: $ python manage.py shell < createusers.py
or     $ python manage.py shell then run exec(open('createusers.py').read()) in shell

"""
from django.contrib.auth.models import User
import pandas as pd
import os
from django.db.utils import IntegrityError
from django.template.loader import render_to_string
from django.core.mail import send_mail, send_mass_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import date, datetime
from blog.views import get_brief, get_event_day
import json

CSV_FILE = 'test.csv'

def password_generator(size):
    import random
    import string
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))

def create_username(firstname, surname):
    username = f'{firstname}_{surname}' 
    return username.lower()

a_day = get_event_day()
brief = get_brief()

FROM_EMAIL='30works <info@thirty.works>'
EMAIL_SUBJECT = "Your new 30works account is ready"
EMAIL_BRIEF_SUBJECT = f"30works30days {a_day} Brief"

# read the CSV file
df = pd.read_csv(CSV_FILE)
# datatuple = (
#     (
#         EMAIL_SUBJECT, 
#         EMAIL_MESSAGE.format(df['First Name'][i], create_username(df['First Name'][i], df['Surname'][i]), password_generator(7)), 
#         FROM_EMAIL, 
#         [df['Email'][i]]
#     ) 
#     for i in df.index
# )
# send_mass_mail(datatuple)

for i in df.index:


    try:
        a_day = get_event_day()
        brief = get_brief()
        first_name = df['First Name'][i]
        first_name.strip()
        surname = df['Surname'][i]
        surname.strip()
        email = df['Email'][i]
        username = create_username(first_name, surname)
        password = password_generator(7)
        user = User.objects.create_user(
            username=username, 
            password=password, 
            email=email,
            first_name=first_name,
            last_name=surname
        )
        user.is_superuser = False
        user.is_staff = False
        user.save()

        print(f'Created User: {username}\nEmail: {email}\nPass: {password}\n==========')
        message = render_to_string(
            'email/new_acount_ready.txt',
            {
                'first_name': first_name,
                'email': email,
                'password': password,
            }
        )
        brief_message = render_to_string(
            'email/daily_brief.txt',
            {
                'current_event_day': a_day,
                'brief_of_the_day': brief,
            }
        )   
        brief_message_html = render_to_string(
            'email/daily_brief.html',
            {
                'current_event_day': a_day,
                'brief_of_the_day': brief,
            }
        )     
        send_mail(
            subject=EMAIL_SUBJECT,
            from_email=FROM_EMAIL,
            message=message,
            recipient_list=[email],)

        send_mail(
            subject=EMAIL_BRIEF_SUBJECT,
            from_email=FROM_EMAIL,
            message=brief_message,
            html_message=brief_message_html,
            recipient_list=[email],)        

    except IntegrityError as ie:
        print(ie)
        print(f'Unable to create User: {username}\nEmail: {email}\nPass: {password}\n==========')

print('done!')





# for i, row in df.iterrows():
#     username = row['First Name'] + '_' + row['Surname']
#     email_address = row['Email Address']
#     password = id_generator(10)
#     try:
#         user = User.objects.create_user(username=username, password=password, email=email_address)
#         user.is_superuser = False
#         user.is_staff = False
#         user.save()

#         print('Created User: {}\nEmail: {}\nPass: {}\n=========='.format(username, email_address, password))

#         email_message = "{}".format(EMAIL_MESSAGE)
#         email_message = email_message.format(username, password)
#         email(EMAIL_SUBJECT, email_message, [email_address])

#     except IntegrityError as ie:
#         print(ie)
#         print('Couldnt create User: {}\nEmail: {}\nPass: {}\n=========='.format(username, email_address, password))
