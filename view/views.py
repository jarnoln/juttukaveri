from django.shortcuts import render
from api01.models import Session


# Create your views here.
def index(request):
    return render(template_name="view/index.html", request=None)


def juttukaveri(request):
    return render(template_name="view/juttukaveri.html", request=None)


def sessions(request):
    context = {
        'sessions': Session.objects.all().order_by('created')
    }
    return render(request=request, template_name="view/sessions.html", context=context)
