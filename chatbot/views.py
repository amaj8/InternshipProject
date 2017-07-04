from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from extract import *


class HomeView(TemplateView):
    template_name = "app/home.html"


def final_response(request):
    print "in final response"
    return render(request, "chatbot/finalresponse.html")


@csrf_exempt
def run_script(request):
    action = None
    userInput = None
    chatbotResponse = None
    url = None
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            if action == "run_script":
                keys = ["battery", "camera", "company", "max_battery", "max_screen_size", "memory",
                         "min_battery", "min_screen_size", "network", "os", "price_from", "price_to", "ram",
                        "screen_size"]
                parameters = {}
                for key in keys:
                    value = request.POST["parameters[" + key + "]"]
                    parameters[key] = value
                f = Flip(parameters)
                url = f.extract()
                # request.session['url'] = url
                # return final_response(request)
                print "url: %s" % url
                # return render(request, "chatbot/display.html", context={'url_key': url})
    return render(request, "chatbot/display.html", {'url_key':url})

