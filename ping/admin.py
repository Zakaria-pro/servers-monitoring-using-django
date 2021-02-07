from django.contrib import admin
from ping.models import Network, Status
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User


class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip_adr', 'State', 'exec_date')
    list_filter = ("exec_date",)
    ordering = ['-exec_date']
    actions = []

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


class NetworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip_adr')
    ordering = ['ip_adr']
    def ping_now(self, request, queryset):
        for ipObj in queryset:
            query = [ipObj.id, ipObj.ip_adr]
            #ip_adr = ipObj.ip_adr
            S = Status.pinger(query)
            pingstatus = S[0]
            exec_date = S[1]
            if pingstatus == False :
                Status.notify_u(query[1], exec_date)
        messages.success(
            request, "Le Ping s'est bien passé, Tu peux consulter son etat sur le dashboard\
                      un mail va etre envoyer a chacun de vous au cas ou un serveur est en panne")    
    
    def notify_me(self, request, queryset):
        from django.core.mail import send_mail
        send_mail(
            'Network State',
            'The ping was good',
            'zhamedoun1@gmail.com',
            ['zhamedoun1@gmail.com'],
            fail_silently=False,
        )
    actions = [ping_now]


# change the template
from django_celery_beat.admin import PeriodicTaskAdmin
from django_celery_beat.models import IntervalSchedule, ClockedSchedule, SolarSchedule, PeriodicTasks, PeriodicTask
class PeriodicTaskAdmin(admin.ModelAdmin): 
    list_display = ('name','enabled','crontab' , 'last_run_at', 'total_run_count')
    ordering = ['last_run_at']
    actions = ['toggle_tasks'] 

# Register and unregister models
from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.unregister(Group)
admin.site.unregister(ClockedSchedule)  
admin.site.unregister(SolarSchedule)  
admin.site.unregister(IntervalSchedule)
admin.site.register(Status, StatusAdmin)
admin.site.register(Network, NetworkAdmin)
