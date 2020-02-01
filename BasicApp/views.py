from django.shortcuts import render

from django.http import HttpResponse


def home(request):
    return HttpResponse("Hello, world. This is BasicApp index.")

    template = loader.get_template('gezi/index.html')

    return HttpResponse(template.render(request))    