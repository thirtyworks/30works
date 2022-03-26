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
from django.core.management.base import BaseCommand

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Gets private data from '30works.json' file. FILE MOST BE IN ROOT DIRECTORY.
config_file = os.path.join(BASE_DIR, '30works.json')
with open(config_file, 'r') as f:
    config_json = json.load(f)


FROM_EMAIL='30works <info@thirty.works>'
EMAIL_FIRST_COM_SUBJECT = "Oh noooo…claim your free pass!"
EMAIL_FINAL_COM_SUBJECT = "Oh noooo…sad to see you go"

def email(subject, message, recipient_list):
    email_from = settings.EMAIL_HOST_USER
    send_mail( subject, message, email_from, recipient_list )


# @kronos.register('38 10 * * *')
# def test_send():
#     t = timezone.localtime().strftime('%d-%m-%Y, %X')
#     message = f'Its {t} now!'
#     send_mail('test_subject', message, 'info@thirtyworks', ['TEST123@gmail.com'])
#     print('done')

# # @kronos.register('15 15 * * *') # set to 3:15 PM for testing
# @kronos.register('20 0 * * *') # set to 20 past midnight
# def daily_emails():
#     # rejected_users = []
#     # accepted_users = []
#     latest_day = get_event_day() 
#     if latest_day > 30:
#         return 'Event is over!'
#     print(f'The day is now: {latest_day}')
#     brief = get_brief()
#     print(f'Brief is: {brief}')
#     EMAIL_BRIEF_SUBJECT = f"30works30days {latest_day} Brief"
#     previous_day = 1 if latest_day - 1 <= 0 else latest_day - 1
#     authors_that_posted = [post.author.email for post in Post.objects.filter(day__number=previous_day, author__is_active=True, author__is_staff=False).distinct('author')]  
#     print(authors_that_posted)
#     print('Total unique post of the day: ' + str(len(authors_that_posted)))    
#     # for post in posts:
#     #     authors_who_submitted_today.append(post.author.username)
#     #     print(post.title)
#     users = [user.user.email for user in UserProfile.objects.filter(user__is_active=True, user__is_staff=False, blocked=False)]
#     for user_email in users:
#         if user_email in authors_that_posted:
#             # Accepted
#             brief_message = render_to_string(
#             'email/daily_brief.txt',
#                 {
#                     'current_event_day': latest_day,
#                     'brief_of_the_day': brief,
#                 }
#             )   
#             brief_message_html = render_to_string(
#             'email/daily_brief.html',
#                 {
#                     'current_event_day': latest_day,
#                     'brief_of_the_day': brief,
#                 }
#             ) 
#             send_mail(
#                 subject=EMAIL_BRIEF_SUBJECT,
#                 from_email=FROM_EMAIL,
#                 message=brief_message,
#                 html_message=brief_message_html,
#                 recipient_list=[user_email],
#             )    
#             print(f'{user_email} is accepted.')         
#         else:
#             # Rejected
#             user = UserProfile.objects.get(user__email=user_email)           
#             user.user.is_active = False
#             user.user.save()
#             user.blocked = True
#             user.date_blocked = datetime.now()
#             user.save()
#             com_message = render_to_string('email/final_commiseration.txt')   
#             com_message_html = render_to_string('email/final_commiseration.html')
#             send_mail(
#                 subject=EMAIL_FINAL_COM_SUBJECT,
#                 from_email=FROM_EMAIL,
#                 message=com_message,
#                 html_message=com_message_html,
#                 recipient_list=[user_email],
#             ) 
#             print(f'{user_email} is rejected!') 


# # @kronos.register('10 13 * * *') 
# def test_sending():
#     # rejected_users = []
#     # accepted_users = []
#     latest_day = 3
#     t = timezone.localtime().strftime('%d-%m-%Y, %X')
#     message = f'Its {t} now!'
#     # print(timezone.now().strftime('%d-%m-%Y, %X') )
#     print(f'The day is now: {latest_day}')
#     brief = 'Can you make a tool to help you to make your work?'
#     print(f'Brief is: {brief}')
#     EMAIL_BRIEF_SUBJECT = f"30works30days {latest_day} Brief - At {t}"
#     previous_day = 1 if latest_day - 1 <= 0 else latest_day - 1
#     print(f'Yesturday was: {previous_day}')
#     authors_that_posted = ['ABC@gmail.com', 'info@12ocollective.com']
#     print('Total unique post of the day: ' + str(len(authors_that_posted)))  
#     # for post in posts:
#     #     authors_who_submitted_today.append(post.author.username)
#     #     print(post.title)
#     users = ['ABC@gmail.com', 'info@12ocollective.com']
#     for user_email in users:
#         if user_email in authors_that_posted:
#             # Accepted
#             brief_message = render_to_string(
#             'email/daily_brief.txt',
#                 {
#                     'current_event_day': latest_day,
#                     'brief_of_the_day': brief,
#                 }
#             )   
#             brief_message_html = render_to_string(
#             'email/daily_brief.html',
#                 {
#                     'current_event_day': latest_day,
#                     'brief_of_the_day': brief,
#                 }
#             ) 
#             send_mail(
#                 subject=EMAIL_BRIEF_SUBJECT,
#                 from_email=FROM_EMAIL,
#                 message=brief_message,
#                 html_message=brief_message_html,
#                 recipient_list=[user_email],
#             )    
#             print(f'{user_email} is accepted.')         
#         else:
#             # Rejected
#             user = UserProfile.objects.get(user__email=user_email)           
#             user.user.is_active = False
#             user.user.save()
#             user.blocked = True
#             user.date_blocked = datetime.now()
#             user.save()
#             com_message = render_to_string('email/final_commiseration.txt')   
#             com_message_html = render_to_string('email/final_commiseration.html')
#             send_mail(
#                 subject=EMAIL_FINAL_COM_SUBJECT,
#                 from_email=FROM_EMAIL,
#                 message=com_message,
#                 html_message=com_message_html,
#                 recipient_list=[user_email],
#             ) 
#             print(f'{user_email} is rejected!') 

@kronos.register('* * * * *', args={'-l': 'nb'})
class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '-l', '--language',
            dest='language',
            type=str,
            default='en',
        )

    def handle(self, *args, **options):
        if options['language'] == 'en':
          print('Hello, world!')

        if options['language'] == 'nb':
          print('Hei, verden!')