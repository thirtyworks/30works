import kronos
import random
from blog.models import Day, Post
from users.models import UserProfile
from django.core.mail import send_mail
from django.conf import settings
import os
import json
from datetime import datetime
import time
from blog.views import get_brief, get_event_day

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config_file = os.path.join(BASE_DIR, '30works.json')
with open(config_file, 'r') as f:
    config_json = json.load(f)

this_event_day = get_event_day()
brief = get_brief()


FROM_EMAIL='30works <info@thirty.works>'
EMAIL_BRIEF_SUBJECT = f"30works30days {this_event_day} Brief"
EMAIL_FIRST_COM_SUBJECT = "Oh noooo…claim your free pass!"
EMAIL_FINAL_COM_SUBJECT = "Oh noooo…sad to see you go"

def email(subject, message, recipient_list):
    email_from = settings.EMAIL_HOST_USER
    send_mail( subject, message, email_from, recipient_list )

@kronos.register('* * * * *')
def test():
    complaints = [
        "I forgot to migrate our applications's cron jobs to our new server! Darn!",
        "I'm out of complaints! Damnit!"
    ]

    print (random.choice(complaints))

@kronos.register('*/2 * * * *')
def test_send():
    send_mail('test_subject', 'test-message', 'info@thirtyworks', ['aaialfa12@gmail.com'])
    print('done')

# @kronos.register('15 15 * * *') # set to 3:15 PM for testing
@kronos.register('* * * * *') # set to 5 past midnight
def daily_emails():
    rejected_users = []
    accepted_users = []
    latest_day = get_event_day()
    previous_day = 1 if get_event_day() - 1 <= 0 else get_event_day() - 1
    authors_that_posted = [post.author.id for post in Post.objects.filter(day=1, author__is_active=True).distinct('author__email')]
    for post in posts:
        authors_who_submitted_today.append(post.author.username)
        print(post.title)
    users = [user.id for user in UserProfile.objects.filter(user__is_active=True, user__is_staff=False)]
    print(authors_who_submitted_today)
    for user_id in users:
        if user_id not in authors_that_posted:
            rejected_users.append(user.user.email)
            user = UserProfile.objects.get(user=user_id)
            user.user.is_active = False
            user.user.save()
            user.blocked = True
            user.date_blocked = datetime.now()
            user.save()
        else:
            accepted_users.append(user.user.email)
    day_number = latest_day.number + 1
    day = Day(number=day_number)
    day.save()

    # accepted_subject = "Accepted."
    accepted_subject = "30/30 Day {}".format(day_number)
    accepted_message = "{}".format(DAILY_BRIEF_EMAIL)
    brief = config_json[str(day_number)]
    accepted_message = accepted_message.format(day_number, day_number, brief)

    # rejected_subject = "Rejected."
    rejected_subject = "30/30 - oh noo, our commiserations"
    # rejected_message = "You are being blocked to use the system."
    rejected_message = "{}".format(COMMISERATIONS_EMAIL)
    rejected_message = rejected_message.format(brief)

    # debugging
    # print(accepted_users)
    # print(rejected_users)
    print('accept message: ')
    print(accepted_message)
    print('reject message: ')
    print(rejected_message)

    # email(rejected_subject, rejected_message, rejected_users)
    # print("Email has been sent to rejected users.")
    # email(accepted_subject, accepted_message, accepted_users)
    # print("Email has been sent to active users.")

    # wait to send out emails
    print('Sleeping...')
    time.sleep(300)

    # send email to rejected users
    for i, rejected_user in enumerate(rejected_users):
        if i > 0 and (i % 50) == 0:
            print('Sleeping...')
            time.sleep(720)
        email(rejected_subject, rejected_message, [rejected_user])

    # send email to active users
    for i, accepted_user in enumerate(accepted_users):
        if i > 0 and (i % 50) == 0:
            print('Sleeping...')
            time.sleep(720)
        email(accepted_subject, accepted_message, [accepted_user])

# python manage.py installtasks
# python manage.py showtasks

def a_job():
  print('okay!')