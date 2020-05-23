from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def hello_world_function_app(request):
    return_object = HttpResponse('<h1>hello world!<h1>')
    return return_object
