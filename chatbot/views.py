from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.http.response import JsonResponse
from django.template.loader import render_to_string
from extract import *


params = {}


class HomeView(TemplateView):
    template_name = "app/home.html"


@csrf_exempt
def final_response(request):
    print "in final response"
    action = None
    userInput = None
    chatbotResponse = None
    url = None
    
    if request.method == 'POST' and request.is_ajax():
        if 'action' in request.POST:
            action = request.POST['action']
            if action == "run_script":
                print "action %s" % action
                keys = ["battery", "camera", "company", "max_battery", "max_screen_size", "memory",
                         "min_battery", "min_screen_size", "network", "os", "price_from", "price_to", "ram",
                        "screen_size"]
                parameters = {}
                # global params
                # for key in keys:
                #     value = request.POST["parameters[" + key + "]"]
                #     try:
                #         a = params[key]
                #     except KeyError:
                #         params[key] = value
                # print params
                for key in keys:
                    value = request.POST["parameters[" + key + "]"]
                    parameters[key] = value
                print "params: %s" % parameters
                f = Flip(parameters)
                # f = Flip(params)
                url = f.extract()
                # request.session['url'] = url
                # return final_response(request)
                print "url: %s" % url
                context={'url_key': url}
                print context
                #return render(request, "chatbot/display.html", context)
                #return redirect('run_script',url_key=url)
                #return render(request,'chatbot/test.html')
                #return JsonResponse({'url_key':url})

                return render(request, "chatbot/finalresponse.html",context)
                #return render(request,"chatbot/list.html",context = {'item_list':item_list})

    
        

@csrf_exempt
def run_script(request):
    """
    action = None
    userInput = None
    chatbotResponse = None
    url = None
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            if action == "run_script":
                print "action %s" % action
                keys = ["battery", "camera", "company", "max_battery", "max_screen_size", "memory",
                         "min_battery", "min_screen_size", "network", "os", "price_from", "price_to", "ram",
                        "screen_size"]
                parameters = {}
                for key in keys:
                    value = request.POST["parameters[" + key + "]"]
                    parameters[key] = value
                f = Flip(parameters)
                url = f.extract()
                request.session['url'] = url
                #return final_response(request)
                print "url: %s" % url
                context={'url_key': url}
                print context
                #return render(request, "chatbot/display.html", context)
                #return redirect('run_script',url_key=url)
                #return render(request,'chatbot/test.html')
                return JsonResponse({'url_key':'url'})
    """
    return render(request, "chatbot/display.html")

