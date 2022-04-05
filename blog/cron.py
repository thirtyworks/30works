import kronos
import random
from blog.models import Day, Post
from users.models import UserProfile
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import os
import json
from datetime import datetime
import time
from blog.views import get_brief, get_event_day
from django.utils import timezone
import pandas as pd
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Gets private data from '30works.json' file. FILE MOST BE IN ROOT DIRECTORY.
config_file = os.path.join(BASE_DIR, '30works.json')
with open(config_file, 'r') as f:
    config_json = json.load(f)

CSV_FILE = os.path.join(BASE_DIR, 'data.csv')

FROM_EMAIL='30works <info@thirty.works>'
EMAIL_FIRST_COM_SUBJECT = "Oh noooo…claim your free pass!"
EMAIL_FINAL_COM_SUBJECT = "Oh noooo…sad to see you go"

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
            print(f'Unable to create\nUser: {username}\nEmail: {email}\nPass: {password}\n==========')

    print('done!')
    
def email(subject, message, recipient_list):
    email_from = settings.EMAIL_HOST_USER
    send_mail( subject, message, email_from, recipient_list )


@kronos.register('38 10 * * *')
def test_send():
    t = timezone.now().strftime('%d-%m-%Y, %X')
    message = f'Its {t} now!'
    send_mail('test_subject', message, 'info@thirtyworks', ['TEST123@gmail.com'])
    print('done')

# @kronos.register('* * * * *')
def test_sending_random_brief_every_minute():
    random_number = random.randint(1, 30)
    latest_day = random_number
    brief = get_brief(random_number)   
    print(f'Brief is: {brief}')
    CSV_FILE = os.path.join(BASE_DIR, 'test.csv')
    df = pd.read_csv(CSV_FILE)

    for i in df.index:
        first_name = df['first_name'][i].strip()
        email = df['email'][i].strip()
        t = timezone.now().strftime('%d-%m-%Y, %X')
        message = f"""
            Hello {first_name},\n
            This is the test email. \n\n
            The brief is: {brief}\n
            Its {t} now!\n\n
            bye.
        """
        send_mail(f'test brief Day {latest_day}', message, 'info@thirtyworks', [email])
    print('done')

@kronos.register('20 0 * * *') # set to 20 past midnight
def daily_emails():
    latest_day = get_event_day() 
    if latest_day == 1:
        print('Creating acounts and sending first brief to participants..')
        create_users_and_send_emails()
        return 'Day 1 is over!'
    if latest_day > 30:
        return 'Event is over!'
    print(f'The day is now: {latest_day}')
    brief = get_brief()
    print(f'Brief is: {brief}')
    EMAIL_BRIEF_SUBJECT = f"30works30days {latest_day} Brief"
    previous_day = 1 if latest_day - 1 <= 0 else latest_day - 1
    authors_that_posted = [post.author.email for post in Post.objects.filter(day__number=previous_day, author__is_active=True, author__is_staff=False).distinct('author')]  
    print(authors_that_posted)
    print('Total unique post of the day: ' + str(len(authors_that_posted)))    
    # for post in posts:
    #     authors_who_submitted_today.append(post.author.username)
    #     print(post.title)
    users = [user.user.email for user in UserProfile.objects.filter(user__is_active=True, user__is_staff=False, blocked=False)]
    for user_email in users:
        if user_email in authors_that_posted:
            # Accepted
            brief_message = render_to_string(
            'email/daily_brief.txt',
                {
                    'current_event_day': latest_day,
                    'brief_of_the_day': brief,
                }
            )   
            brief_message_html = render_to_string(
            'email/daily_brief.html',
                {
                    'current_event_day': latest_day,
                    'brief_of_the_day': brief,
                }
            ) 
            send_mail(
                subject=EMAIL_BRIEF_SUBJECT,
                from_email=FROM_EMAIL,
                message=brief_message,
                html_message=brief_message_html,
                recipient_list=[user_email],
            )    
            print(f'{user_email} is accepted.')         
        else:
            # Rejected
            user = UserProfile.objects.get(user__email=user_email)           
            user.user.is_active = False
            user.user.save()
            user.blocked = True
            user.date_blocked = datetime.now()
            user.save()
            com_message = render_to_string('email/final_commiseration.txt')   
            com_message_html = render_to_string('email/final_commiseration.html')
            send_mail(
                subject=EMAIL_FINAL_COM_SUBJECT,
                from_email=FROM_EMAIL,
                message=com_message,
                html_message=com_message_html,
                recipient_list=[user_email],
            ) 
            print(f'{user_email} is rejected!') 
