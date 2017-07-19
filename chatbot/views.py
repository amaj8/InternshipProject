from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from extract import *


params = {}


@csrf_exempt
def final_response(request):
    if request.method == 'POST' and request.is_ajax():
        if 'action' in request.POST:
            action = request.POST['action']
            if action == "run_script":
                print "action %s" % action
                keys = ["battery", "camera", "company", "max_battery", "max_screen_size", "memory",
                         "min_battery", "min_screen_size", "network", "os", "price_from", "price_to", "ram",
                        "screen_size"]
                parameters = {}
                for key in keys:
                    try:
                        value = request.POST["parameters[" + key + "]"]
                        parameters[key] = value
                    except:
                        continue
                print "params: %s" % parameters
                f = Flip(parameters)
                item_list = f.extract()
                return render(request,"chatbot/list.html",context = {'item_list':item_list})


@csrf_exempt
def run_script(request):
    return render(request, "chatbot/display.html")

