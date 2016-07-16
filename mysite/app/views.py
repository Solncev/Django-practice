
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from django.shortcuts import render_to_response
from django.template.context import RequestContext

# def index(request):
#     return render_to_response("app/index.html", context_instance=RequestContext(request))

def index(request):
    return render(request, 'app/index.html')

# def index(request):
#     template = loader.get_template('app/index.html')
#     return HttpResponse(template)
