from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response
from django.template import RequestContext



class IndexView(TemplateView):
    template_name = 'index.html'

    def home_page(request):
        return render_to_response('index.html', {}, context_instance=RequestContext(request))