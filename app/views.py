# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.views.generic import TemplateView
from extract import *

class HomeView(TemplateView):
    template_name = "app/home.html"

def extract(request
    #this is just a demo req dictionary.
    #req is a dictionary which will store all the vars for user requirements from the json dumps
    #insert code for extraction of the dictionary from the json dump
    req = {'company':'Lenovo','price_to':'20000','ram':'2','network':'4G'}
    f = Flip(req)
    item_list = f.extract()
    return render(request,'app/list.html',context = {'item_list':item_list})
