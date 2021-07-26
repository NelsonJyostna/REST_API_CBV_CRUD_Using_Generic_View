from .models import Task
from django.views.generic import View
import io
from rest_framework.parsers import JSONParser
from .serializers import TaskSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# https://stackoverflow.com/questions/35669322/difference-between-jsonparser-and-jsonrenderer

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class TaskCBV(View):
    def get(self, request, *args, **kwargs):
        json_data=request.body
        stream=io.BytesIO(json_data)
        data=JSONParser().parse(stream)   #JSONParser is responsible of converting JSON to dictionary.
        id=data.get('id', None)
        if id is not None:
            tsk = Task.objects.get(id=id)
            serializer= TaskSerializer(tsk)
            json_data = JSONRenderer().render(serializer.data) #JSONRenderer convert dict to JSON and its implemented inside Response class
            return HttpResponse(json_data, content_type='application/json')
        qs = Task.objects.all()
        serializer=TaskSerializer(qs, many=True) 
        json_data= JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')

    def post(self, request, *args, **kwargs):
        json_data=request.body
        stream=io.BytesIO(json_data)
        data= JSONParser().parse(stream)
        serializer= TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            msg={'msg':"Resource crreated Successfully"}
            json_data=JSONRenderer().render(msg)
            return HttpResponse(json_data, content_type='application/json')

        json_data= JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')    


    def put(self, request, *args, **kwargs):
        json_data=request.body
        stream=io.BytesIO(json_data)
        data=JSONParser().parse(stream)
        id=data.get('id')
        tsk=Task.objects.get(id=id)
        serializer=TaskSerializer(tsk, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            msg={'msg': 'Resources updated successfully'}
            json_data=JSONRenderer().render(msg)
            return HttpResponse(json_data, content_type='application/json')
        json_data=JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')

    def delete(self, request, *args, **kwargs):
        json_data=request.body
        stream=io.BytesIO(json_data)
        data=JSONParser().parse(stream)
        id=data.get('id', None)
        if id is not None:
            tsk=Task.objects.get(id=id)
            tsk.delete()
            msg={'msg' :'Resource deleted successfully'}
            json_data=JSONRenderer().render(msg)
            return HttpResponse(json_data, content_type='application/json')
        msg={'msg':'plz provide the id'}
        json_data=JSONRenderer().render(msg)
        return HttpResponse(json_data, content_type='application_json')           
