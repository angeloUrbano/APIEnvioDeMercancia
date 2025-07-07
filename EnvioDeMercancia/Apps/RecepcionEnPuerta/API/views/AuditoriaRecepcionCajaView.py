#rest framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView


#propias
from EnvioDeMercancia.Apps.RecepcionEnPuerta.models import CajasAlmacenadas


# serializer 

from EnvioDeMercancia.Apps.RecepcionEnPuerta.API.serializers.AuditoriaRecepcionSerializer import CajasAlmacenadasHistoricalSerializer

class AuditoriaRecepcionEnPuerta(ListAPIView):
    serializer_class = CajasAlmacenadasHistoricalSerializer
    queryset = serializer_class.Meta.model.objects.all()



    
