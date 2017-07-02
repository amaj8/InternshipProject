from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from extract import *


class HomeView(TemplateView):
    template_name = "app/home.html"


@csrf_exempt
def run_script(request):
    context = None
    action = None
    userInput = None
    chatbotResponse = None
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            if action == "run_script":
                keys = [ "battery","camera","company","max_battery","max_screen_size","memory",
                         "min_battery","min_screen_size","network","os", "price_from","price_to","ram","screen_size"]
                parameters = {}
                for key in keys:
                    value = request.POST["parameters[" + key + "]"]
                    parameters[key]=value.strip()
                print "parameters: %s" % parameters
        else:
            print "no response"
    return render(request, "chatbot/display.html")


def extract(request):
    #this is just a demo req dictionary.
    #req is a dictionary which will store all the vars for user requirements from the json dumps
    #insert code for extraction of the dictionary from the json dump
    req = {'company':'Lenovo','price_to':'20000','ram':'2','network':'4G'}
    f = Flip(req)
    item_list = f.extract()
    return render(request,'app/list.html',context = {'item_list':item_list})
