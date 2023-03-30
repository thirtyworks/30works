"""
Usage: $ python manage.py shell < createusers.py
or     $ python manage.py shell then run exec(open('createusers.py').read()) in shell

"""
from django.contrib.auth.models import User
import pandas as pd
from django.db.utils import IntegrityError
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.template.loader import render_to_string
from blog.views import get_brief, get_event_day

CSV_FILE = 'data.csv'

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
EMAIL_SUBJECT = "Your new 30works30days account is ready"
EMAIL_BRIEF_SUBJECT = f"30works30days {a_day} Brief"


def create_users_and_send_emails():
# read the CSV file
    df = pd.read_csv(CSV_FILE)

    for i in df.index:
        try:
            a_day = get_event_day()
            brief = get_brief()
            first_name = df['first_name'][i].strip()
            last_name = df['last_name'][i].strip()
            email = df['email'][i].strip()
            username = create_username(first_name, last_name)
            password = password_generator(7)
            user = User.objects.create_user(
                username=username, 
                password=password, 
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.is_superuser = False
            user.is_staff = False
            user.save()

            print(f'Created User: {username}\nEmail: {email}\nPass: {password}\n==========')
            message = render_to_string(
                'email/new_acount_ready.txt',
                {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'password': password,
                }
            )
            message_html = render_to_string(
                'email/new_acount_ready.html',
                {
                    'first_name': first_name,
                    'last_name': last_name,
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
                html_message=message_html,
                recipient_list=[email],
            )

            # send_mail(
            #     subject=EMAIL_BRIEF_SUBJECT,
            #     from_email=FROM_EMAIL,
            #     message=brief_message,
            #     html_message=brief_message_html,
            #     recipient_list=[email],)        

        except IntegrityError as ie:
            print(ie)
            print(f'Unable to create\nUser: {username}\nEmail: {email}\nPass: {password}\n==========')

    print('done!')

create_users_and_send_emails()