from django.shortcuts import render


# Create your views here.
def index(request):
    return render(template_name='view/juttukaveri.html', request=None)
