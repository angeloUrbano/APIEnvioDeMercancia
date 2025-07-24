#rest framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from EnvioDeMercancia.Apps.Client.API.SOLID.service import AudicotiriaClientsService

from EnvioDeMercancia.Apps.Client.API.serializers.AuditoriaSerializer.AuditoriaClientSerializer import ClientNaturalHistoricalSerializer



@api_view(['GET'])
def AuditClietsView(request):

    if request.method=="GET":
        model_selected = "natural" # si son mas modelos se puede enviar que modelo se va seleccionar por la peticion
        if not model_selected:
            return Response({"message":"error en modelo seleccionado"} , status= status.HTTP_400_BAD_REQUEST)

        try:
            data = AudicotiriaClientsService.get_listado_cliente(model_selected)
            return Response(data, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    