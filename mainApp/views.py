from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import os

def template_test(request):
    return render(request, 'example.html')

# test