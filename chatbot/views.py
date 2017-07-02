from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def run_script(request):
    context = None
    action = None
    userInput = None
    chatbotResponse = None
    request.session.set_expiry(0)
    # request.POST['userInput'] = []
    if request.method == 'POST':
        if 'action' and 'parameters' in request.POST:
            action = request.POST['action']
            parameters = request.POST['parameters']
        else:
            print "no action"
        if 'userInput' and 'chatbotResponse' in request.POST:
            userInput = request.POST['userInput']
            chatbotResponse = request.POST['chatbotResponse']
            # request.session['userInput'].append(userInput)
            # request.session['chatbotResponse'].append(chatbotResponse)
        else:
            print "no response"
        context = {'action': action, 'userInput': userInput, 'chatbotResponse': chatbotResponse}
    return render(request, "chatbot/display.html", context=context)


# def display(request):
#     context = request.session['context']
#     return render(request, "chatbot/display.html", context=context)
