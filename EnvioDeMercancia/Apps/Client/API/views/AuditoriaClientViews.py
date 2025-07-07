#rest framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from EnvioDeMercancia.Apps.Client.API.SOLID.service import AudicotiriaClientsService


@api_view(['GET'])
def AuditClietsView(request):
    if request.method=="GET":

        model_selected = request.headers.get("Tipo-Cliente")
        if not model_selected:
            return Response({"message":"error en modelo seleccionado"} , status= status.HTTP_400_BAD_REQUEST)

        try:
            # Nota: Ahora llamamos al método de clase correctamente
            data = AudicotiriaClientsService.get_listado_cliente(model_selected)
            return Response(data, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    