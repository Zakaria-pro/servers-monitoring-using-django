from celery import Celery
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from django.core.wsgi import get_wsgi_application
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Dashy.settings")


application = get_wsgi_application()



app = Celery('tasks', broker='amqp://localhost')

# @app.task
# def add(x,y):
#     return x+y

from ping.models import Status, check_ping
from django.utils import timezone
from django.core.mail import send_mail

@periodic_task(run_every=(crontab(minute='*/1')), name="Ping", ignore_result=True)
def Ping():
    ip_adr = "192.168.1.104"
    pingstatus = check_ping(ip_adr)
    S = Status(ip_adr_id=9, State=pingstatus, exec_date=timezone.now())
    S.save()
    if pingstatus == False :
        message = "Le serveur qui a cette adresse IP : "+ip_adr+" est en pane.\nLe ping c'est fait le "+timezone.now().strftime("%m/%d/%Y, %H:%M:%S")
        send_mail(
            'Network State',
            message,
            'zhamedoun1@gmail.com',
            ['zhamedoun1@gmail.com'],
            fail_silently=False,
        )


    










    #Status.ping_auto()

# @app.task
# def ping():
#     #ip_adr = ipObj.ip_adr
#     Status.ping_auto()
       