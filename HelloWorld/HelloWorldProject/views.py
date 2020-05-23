from django.http import HttpResponse
from django.views.generic.base import TemplateView


def hello_world_function(request):
    return_object = HttpResponse('<h1>hello world<h1>')
    return return_object


class HelloWorldView(TemplateView):
    template_name = 'hello.html'