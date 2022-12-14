from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth import get_user_model

def send_proposal_reminder_email(users_without_proposal):
    subject = 'Foco Krispis - You have not submitted your proposal yet!'
    message = 'You have not submitted your proposal yet! Please do it now!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email for user in users_without_proposal]
    send_mail( subject, message, email_from, recipient_list )

def send_results_email(winner, tomorrow):
    subject = f'Foco Krispis - Results for {tomorrow}'
    message = f'The winner dish is {winner.title} with {winner.number_of_votes} votes!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email for user in get_user_model().objects.all()]
    send_mail( subject, message, email_from, recipient_list )
    
def send_vote_notification_email():
    subject = 'Foco Krispis - You can vote now!'
    message = 'All users have submitted their proposals. You can vote now!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email for user in get_user_model().objects.all()]
    send_mail( subject, message, email_from, recipient_list )

