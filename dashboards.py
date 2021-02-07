from controlcenter import Dashboard, widgets
from ping.models import Network, Status
from controlcenter.widgets.contrib import simple 
from Dashy import settings
from django.utils import timezone
import django.contrib.admin.widgets as ad
import datetime
from django.db.models import Count
from django.utils import timezone
from polls.models import Order, Pizza, Restaurant


#----------------------------------------------    

# Widget : Double Bar Chart
class RestaurantSingleBarChart(widgets.SingleBarChart):
    width=widgets.SMALL
    # Displays score of each restaurant.
    title = 'Most popular restaurant'
    model = Restaurant
    class Chartist:
        options = {
            # Displays only integer values on y-axis
            'onlyInteger': True,
            # Visual tuning
            'chartPadding': {
                'top': 24,
                'right': 0,
                'bottom': 0,
                'left': 0,
            }
        }

    def legend(self):
        # Duplicates series in legend, because Chartist.js
        # doesn't display values on bars
        return self.series

    def values(self):
        # Returns pairs of restaurant names and order count.
        queryset = self.get_queryset()
        return (queryset.values_list('name')
                        .annotate(baked=Count('orders'))
                        .order_by('-baked')[:self.limit_to])

# Widget Single Bar Chart  
class MySingleBarChart(widgets.SingleBarChart):
    width=widgets.SMALL
    # Displays score of each restaurant.
    title = 'Single One'
    model = Pizza
    class Chartist:
        options = {
            # Displays only integer values on y-axis
            'onlyInteger': True,
            # Visual tuning
            'chartPadding': {
                'top': 24,
                'right': 0,
                'bottom': 0,
                'left': 0,
            }
        }

    def legend(self):
        # Duplicates series in legend, because Chartist.js
        # doesn't display values on bars
        return self.series

    def values(self):
        # Returns pairs of restaurant names and order count.
        queryset = self.get_queryset()
        return (queryset.values_list('name')
                        .annotate(baked=Count('orders'))
                        .order_by('-baked')[:self.limit_to])



# Widget : List 
from collections import namedtuple
class widg(widgets.ItemList):
    #model = P
    #queryset = model.objects.all()
    list_display = ('name','age','DOB')
    # Python code to demonstrate namedtuple()  
    # Declaring namedtuple()   
    # Adding values   
       
    #list_display = Student
    def get_queryset(self):
        Student = namedtuple('Student',['name','age','DOB'])
        S1 = Student('Nandini','19','2541997') 
        S2 = Student('Zaka','21','2541997') 
        S3 = Student('Mohamed','19','2541997') 
        S = [S1, S2, S3]  
        return S


# Widget : My Network
class my_network(widgets.ItemList):
    title = 'Nos Serveurs'
    list_display = ('id','ip_adr')
    model = Network
    queryset = model.objects.all()
    changelist_url = model
    
# Widget Ping :
class ping(widgets.ItemList):
    model = Status
    title = 'Etat des Serveurs'
    subtitle = 'True : On ------------ False : OFF'
    changelist_url = model, {'status__exact': 0, 'o': '-7.-1'}
    #model.pinger()
    #for entry in model.objects.all():
    queryset = model.objects.all().order_by('-exec_date')[:4]
    list_display = ('ip_adr_id','exec_date', "State")



# Widget 3
class Documentation(simple.ValueList):
    width = widgets.SMALL
    title = 'Some Usefull links'
    #subtitle = 'For documentation'

    def get_data(self):
        return [
            {'label': 'QuerySet API', 'url':'https://docs.djangoproject.com/en/3.1/ref/models/querysets/'},
            {'label': 'Django ', 'url':'https://www.djangoproject.com/start/'},
            {'label': 'Django-admin-site ', 'url': 'https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#modeladmin-methods'},
            {'label' : 'ControlCenter ', 'url' : 'https://django-controlcenter.readthedocs.io/en/latest/index.html', 'help_text' : 'not very useful but'}
        ]    


# Widget 4
class AppInfoWidget(simple.KeyValueList):
    width=widgets.SMALL
    title = 'App info'

    def get_data(self):
        return {
            # A simple key-value pair
            #'Installed apps':settings.INSTALLED_APPS,
            'Language ': 'Python',
            'Language code': settings.LANGUAGE_CODE,
            # A dictionary value can be used to display a link
            'Default timezone': {
                'label': settings.TIME_ZONE,
                'url': 'https://docs.djangoproject.com/en/2.1/topics/i18n/timezones/',
            }}





class MyDashboard(Dashboard):
    title = 'DASHBOARD'
    widgets = (
        widgets.Group([ping, my_network], width=widgets.LARGE, height=300),
        MySingleBarChart,
        Documentation,
        AppInfoWidget,
        RestaurantSingleBarChart, 
        )
    class Media:
        css = {
            'chartist-default-colors': 'templates\media\style.css'
        }   
        #js = ("style.js",)

#Status.pinger()