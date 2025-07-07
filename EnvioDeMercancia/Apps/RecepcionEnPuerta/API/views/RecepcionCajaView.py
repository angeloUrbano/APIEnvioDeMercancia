#rest framework
from rest_framework import  viewsets
from rest_framework import status
from rest_framework.response import Response

from rest_framework.generics import (GenericAPIView , ListAPIView , RetrieveAPIView , 
                                     RetrieveUpdateDestroyAPIView , ListCreateAPIView ,
                                     RetrieveAPIView , RetrieveUpdateAPIView)

from rest_framework.views import APIView


#modelo
from EnvioDeMercancia.Apps.RecepcionEnPuerta.models import CajasAlmacenadas


#serializer
from EnvioDeMercancia.Apps.RecepcionEnPuerta.API.serializers.RecepcionSerializers import RecepcionEnPuertaCRUDSerializers


from EnvioDeMercancia.Apps.RecepcionEnPuerta.API.SOLID.service import RecepcionService

class RecepcionEnPuertaCRUD(viewsets.ModelViewSet):
    
    def __init__(self, **kwargs):
        self.service = RecepcionService()
        super().__init__(**kwargs)

    serializer_class = RecepcionEnPuertaCRUDSerializers
    queryset =  CajasAlmacenadas.objects.all()


    #GET ALL boxes
    def list(self  , request):
        serializer = self.service.serializer_all_boxes(self.serializer_class)
        if serializer["success"]:
            return Response(serializer["info"] , status=status.HTTP_200_OK)
        return Response( {"error":"error obteniendo listado de cajas"}, status=status.HTTP_400_BAD_REQUEST)   

    # create 
    def create(self , request):
        serializer = self.service.serializer_create_box( serializer_class=self.serializer_class , request = request.data)

        if serializer["success"]:
            return Response(serializer["info"], status=status.HTTP_200_OK)
        return Response(serializer["info"] , status=status.HTTP_400_BAD_REQUEST)   

    #delete  
    def destroy(self , request , pk=None):
        box =  self.service.serializer_delete_box(pk = self.kwargs["pk"] , serializer_class = self.serializer_class)

        if box["success"]:
            return Response( box["info"], status=status.HTTP_200_OK)
        return Response(box["info"] , status=status.HTTP_400_BAD_REQUEST)

    #update 
    def update(self , request , pk=None): 
        serializer = self.service.serializer_update_box(pk = self.kwargs["pk"] , serializer_class=self.serializer_class , request = request.data)
        if serializer["success"]:
            return Response(serializer["info"] , status=status.HTTP_200_OK)
        return Response(serializer["info"] , status=status.HTTP_400_BAD_REQUEST)   


    #this function get just one box
    def retrieve (self , request , pk=None):

        serializer = self.service.serializer_one_boxes(pk = self.kwargs["pk"] , serializer_class=self.serializer_class)
        if serializer["success"]:
            return Response(serializer["info"] , status=status.HTTP_200_OK)
        return Response({"error":"error obteniendo box"} , status=status.HTTP_400_BAD_REQUEST)  
