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
from blog.views import get_brief, get_event_day, get_event_day_with_limit
from django.utils import timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config_file = os.path.join(BASE_DIR, '30works.json')
with open(config_file, 'r') as f:
    config_json = json.load(f)



FROM_EMAIL='30works <info@thirty.works>'
EMAIL_FIRST_COM_SUBJECT = "Oh noooo…claim your free pass!"
EMAIL_FINAL_COM_SUBJECT = "Oh noooo…sad to see you go"

def email(subject, message, recipient_list):
    email_from = settings.EMAIL_HOST_USER
    send_mail( subject, message, email_from, recipient_list )

# @kronos.register('* * * * *')
# def test():
#     complaints = [
#         "I forgot to migrate our applications's cron jobs to our new server! Darn!",
#         "I'm out of complaints! Damnit!"
#     ]

#     print (random.choice(complaints))

@kronos.register('38 10 * * *')
def test_send():
    t = timezone.localtime().strftime('%d-%m-%Y, %X')
    message = f'Its {t} now!'
    send_mail('test_subject', message, 'info@thirtyworks', ['TEST123@gmail.com'])
    print('done')

# @kronos.register('15 15 * * *') # set to 3:15 PM for testing
@kronos.register('20 0 * * *') # set to 20 past midnight
def daily_emails():
    # rejected_users = []
    # accepted_users = []
    check_event = get_event_day_with_limit() 
    if check_event > 30:
        return 'Event is over!'
    latest_day = get_event_day()
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


# @kronos.register('10 13 * * *') 
def test_sending():
    # rejected_users = []
    # accepted_users = []
    latest_day = 3
    t = timezone.localtime().strftime('%d-%m-%Y, %X')
    message = f'Its {t} now!'
    # print(timezone.now().strftime('%d-%m-%Y, %X') )
    print(f'The day is now: {latest_day}')
    brief = 'Can you make a tool to help you to make your work?'
    print(f'Brief is: {brief}')
    EMAIL_BRIEF_SUBJECT = f"30works30days {latest_day} Brief - At {t}"
    previous_day = 1 if latest_day - 1 <= 0 else latest_day - 1
    print(f'Yesturday was: {previous_day}')
    authors_that_posted = ['ABC@gmail.com', 'info@12ocollective.com']
    print('Total unique post of the day: ' + str(len(authors_that_posted)))  
    # for post in posts:
    #     authors_who_submitted_today.append(post.author.username)
    #     print(post.title)
    users = ['ABC@gmail.com', 'info@12ocollective.com']
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

    # day_number = latest_day.number + 1
    # day = Day(number=day_number)
    # # day.save()

    # # accepted_subject = "Accepted."
    # accepted_subject = "30/30 Day {}".format(day_number)
    # accepted_message = "{}".format(DAILY_BRIEF_EMAIL)
    # brief = config_json[str(day_number)]
    # accepted_message = accepted_message.format(day_number, day_number, brief)

    # # rejected_subject = "Rejected."
    # rejected_subject = "30/30 - oh noo, our commiserations"
    # # rejected_message = "You are being blocked to use the system."
    # rejected_message = "{}".format(COMMISERATIONS_EMAIL)
    # rejected_message = rejected_message.format(brief)

    # # debugging
    # # print(accepted_users)
    # # print(rejected_users)
    # print('accept message: ')
    # print(accepted_message)
    # print('reject message: ')
    # print(rejected_message)

    # # email(rejected_subject, rejected_message, rejected_users)
    # # print("Email has been sent to rejected users.")
    # # email(accepted_subject, accepted_message, accepted_users)
    # # print("Email has been sent to active users.")

    # # wait to send out emails
    # print('Sleeping...')
    # time.sleep(300)

    # # send email to rejected users
    # for i, rejected_user in enumerate(rejected_users):
    #     if i > 0 and (i % 50) == 0:
    #         print('Sleeping...')
    #         time.sleep(720)
    #     email(rejected_subject, rejected_message, [rejected_user])

    # # send email to active users
    # for i, accepted_user in enumerate(accepted_users):
    #     if i > 0 and (i % 50) == 0:
    #         print('Sleeping...')
    #         time.sleep(720)
    #     email(accepted_subject, accepted_message, [accepted_user])

# python manage.py installtasks
# python manage.py showtasks

def a_job(day):
    # testing logic
    print('event is', get_event_day_with_limit() )
    check_event = day
    if check_event > 30:
        return 'Event is over!'
    else:
        return 'Still on-going!'