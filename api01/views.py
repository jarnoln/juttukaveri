from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from django.http import JsonResponse


@api_view(['POST'])
def submit_audio_file(request):
    """ Submit resume """
    audio_file = request.FILES['audio_file']
    print('audio file=%s' % audio_file)
    # file_content = resume_file.read()
    # data = json.loads(file_content.decode('utf-8'))
    return JsonResponse({})


@api_view(['POST'])
def submit_audio(request):
    """ Submit resume """
    print('request.data=%s' % request.data)
    audio = request.data['audio']
    return Response('tadaa!')
