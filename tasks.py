""" This file contains periodic tasks running in the background. """

import os
from celery import Celery
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from django.core.wsgi import get_wsgi_application
from ping.models import Status, check_ping
from django.utils import timezone
from django.core.mail import send_mail

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Dashy.settings")
application = get_wsgi_application()
app = Celery('tasks', broker='amqp://localhost')

# Ping every minute on servers
@periodic_task(run_every=(crontab(minute='*/1')), name="Ping", ignore_result=True)
def Ping():
    ip_adr = "192.168.1.104"
    pingstatus = check_ping(ip_adr)   # Ping on the server with this ip_adr

    S = Status(ip_adr_id=9, State=pingstatus, exec_date=timezone.now())
    S.save()   # Save statuts in the database

    # If the server is off send email to admin
    if pingstatus is False:
        message = "Le serveur qui a cette adresse IP : "+ip_adr+"est en pane.\n"\
                  "Le ping c'est fait le "+timezone.now().strftime("%m/%d/%Y, %H:%M:%S")
        send_mail(
            'Network State',
            message,
            'zhamedoun1@gmail.com',  # Sender
            ['zhamedoun1@gmail.com'],  # Reciever
            fail_silently=False,
        )
       
