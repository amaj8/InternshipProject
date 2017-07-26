from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.views.generic import FormView
from website.settings import DEFAULT_FROM_EMAIL
from django.views.decorators.csrf import csrf_exempt
from extract import *
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from .tokens import account_activation_token
from django.contrib.auth.models import User
#from chatbot.forms import SignUpForm
#from .forms import SignUpForm

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, get_user_model
from django.contrib.auth import authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        return redirect('../../../login/')
    else:
        return render(request, 'chatbot/account_activation_invalid.html')
# MAIL SENT FOR ACTIVATION
def account_activation_sent(request):
   return render(request, 'chatbot/activate_mail.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your blog account.'
            message = render_to_string('account_activation_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # user.email_user(subject, message)
            toemail = form.cleaned_data.get('email')
            email = EmailMessage(subject, message, to=[toemail])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login_success(request):
    test = request.user.first_name
    test1 = request.user.profile.email_confirmed
    if test1 == True:
        return redirect('chatbot/')
    return render(request, 'chatbot/login_fail.html')

def home(request):
    return render(request, 'home.html')



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

