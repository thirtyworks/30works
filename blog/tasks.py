from celery import shared_task
from django.contrib.auth.models import User
import pandas as pd
import os
from django.db.utils import IntegrityError
from django.template.loader import render_to_string
from django.core.mail import send_mail, send_mass_mail
from django.contrib.auth.models import User

CSV_FILE = 'test.csv'
FROM_EMAIL='30works30days <info@thirty.works>'
EMAIL_SUBJECT = "Your new 30works account is ready"

def password_generator(size):
    import random
    import string
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))

def create_username(firstname, surname):
    username = f'{firstname}_{surname}' 
    return username.lower()

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y

@shared_task
def pswd():
    return password_generator(8)

@shared_task
def send_email():
    df = pd.read_csv('test.csv')
    for i in df.index:

        try:
            first_name = df['First Name'][i]
            first_name.strip()
            surname = df['Surname'][i]
            surname.strip()
            email = df['Email'][i]
            username = create_username(first_name, surname)
            password = password_generator(7)
            # user = User.objects.create_user(
            #     username=username, 
            #     password=password, 
            #     email=email,
            #     first_name=first_name,
            #     last_name=surname
            # )
            # user.is_superuser = False
            # user.is_staff = False
            # user.save()

            print(f'Created User: {username}\nEmail: {email}\nPass: {password}\n==========')
            message = render_to_string(
                'email/new_acount_ready.txt',
                {
                    'first_name': first_name,
                    'email': email,
                    'password': password,
                }
            )
            send_mail(
                subject=EMAIL_SUBJECT,
                from_email=FROM_EMAIL,
                message=message,
                recipient_list=[email],)

        except IntegrityError as ie:
            print(ie)
            print(f'Unable to create User: {username}\nEmail: {email}\nPass: {password}\n==========')
            
    return 'done!'