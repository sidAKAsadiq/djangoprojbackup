from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from main.models import *
from .serializers import *


@api_view(['GET'])
def get_routes(request):
    routes = [
              'GET /api/',
              'GET /api/rooms',     #way to get all rooms from our web app
              'GET /api/rooms/:id', #way to get a specific room from our web app
              ]
    #return JsonResponse(routes , safe=False) # safe(false) will allow routes to be converted into JSON format
    return Response(routes) # safe(false) will allow routes to be converted into JSON format

@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.all() #these rooms need to be converted to json format as they are objects of a model
    serialzer = room_serializer(rooms, many=True) #serializing many objects
    return Response(serialzer.data) #returning serialized rooms (JSON Formatted) data



#for getting a single room
@api_view(['GET'])
def get_room(request,pk):
    room = Room.objects.get(id=pk)
    serialzer = room_serializer(room, many=False) 
    return Response(serialzer.data) 