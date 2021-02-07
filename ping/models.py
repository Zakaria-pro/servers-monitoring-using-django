from django.db import models
from django.utils import timezone
import time
import subprocess
import platform

class Network (models.Model):
    ip_adr = models.GenericIPAddressField(protocol='IPv4', verbose_name="Adresse IP")

    def __str__(self):
        return self.ip_adr

    class Meta:
        verbose_name_plural = "Les serveurs"     

        
def check_ping(current_ip_address):
        try:
            output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower(
            ) == "windows" else 'c', current_ip_address ), shell=True, universal_newlines=True)
            if 'unreachable' in output:
                print('unreachable')
                return False
            else:
                print("rechable")
                return True
        except Exception:
                print("Exception")
                return False

        
class Status(models.Model):
    ip_adr = models.ForeignKey(Network, on_delete=models.CASCADE, verbose_name="Id de l'adresse Ip")
    State = models.BooleanField(default=False, verbose_name="Etat du network", help_text="True Means ON") # zero : the machine is not conected to the network, One: is connected 
    exec_date = models.DateTimeField(verbose_name="Date d'execution du ping")   

    def __str__(self):
        return self.exec_date.strftime('%b/%d/%Y -- %H:%M:%S %Z')

    class Meta:
        verbose_name_plural = "L'état des servers"    

    def pinger(ipObj):  
        pingstatus = check_ping(ipObj[1])   
        S = Status(ip_adr_id=ipObj[0], State=pingstatus, exec_date=timezone.now())
        S.save()
        return [pingstatus, timezone.now()]
        
    # Send Mail     
    def notify_u(ip_adresse, date_execution):
        from django.core.mail import send_mail
        date_exec_str = date_execution.strftime("%m/%d/%Y, %H:%M:%S")
        message = "Le serveur qui a cette adresse IP : "+ip_adresse+" est en pane.\nLe ping c'est fait le "+date_exec_str
        send_mail(
        'Network State',
        message,
        'zhamedoun1@gmail.com',
        ['zhamedoun1@gmail.com'],
        fail_silently=False,
        )

    # Le Ping Automatique 
    def ping_auto():
        ip_adresse = '8.8.8.8'
        pingstatus = check_ping(ip_adresse)   
        S = Status(ip_adr_id=6, State=pingstatus, exec_date=timezone.now())
        S.save()
        if pingstatus == False:
            Status.notify_u(ip_adresse, timezone.now())
