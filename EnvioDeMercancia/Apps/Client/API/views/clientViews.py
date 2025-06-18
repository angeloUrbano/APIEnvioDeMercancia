#rest framework
from rest_framework import  viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (GenericAPIView , ListAPIView , RetrieveAPIView , 
                                     RetrieveUpdateDestroyAPIView , ListCreateAPIView ,
                                     RetrieveAPIView , RetrieveUpdateAPIView)
from rest_framework.views import APIView

from rest_framework.exceptions import NotFound
from django.core.exceptions import ValidationError



#Propias
from EnvioDeMercancia.Apps.Client.models import (
    ClienteUsuarioDestino, 
    ClienteQuienEnvia,
    ClienteQuienRecibe, 
    ClientNatural,
    ClientCourier,
    Direccion
)

#serializers client courier , list create and update
from EnvioDeMercancia.Apps.Client.API.serializers.courierSerializer import GeneralListClientCourierSerializers , ClientCourierCreateSerializer , ClientCourierUpdateSerializer

#serializers client natural , list create and update
from EnvioDeMercancia.Apps.Client.API.serializers.naturalSerializers import  GeneralListClienNaturaltSerializers , ClientNaturalCreateSerializer , ClientNaturalUpdateSerializer

# serializers cliente destino
from EnvioDeMercancia.Apps.Client.API.serializers.clienteDestinoSerializers import ClientCourierDestinoSerializer , ClientCourierDestinoUpdateSerializer

#serializers cliente quien envia
from EnvioDeMercancia.Apps.Client.API.serializers.clienteQuienEnviaSerializers  import ClientNaturalQuienEnviaSerializer, ClientNaturalQuienEnviaUpdateSerializer

#serializers cliente quien recibe
from EnvioDeMercancia.Apps.Client.API.serializers.clienteQuienRecibeSerializers import (
ClientNaturalQuienRecibeSerializer , ClientNaturalQuienRecibeUpdateSerializer
)



from EnvioDeMercancia.Apps.Client.API.SOLID.service import ClienteService , ClienteRelacionadosService



# with this Endpoint i have natural and courier clients whits theirs models related ready to be listed
class GeneraListClients(APIView):
    def __init__(self):
        self.service = ClienteService()
        
    def get (self , request):
        clientes = self.service.list_all_clients()
        
        serialized_data = {
            'naturales': GeneralListClienNaturaltSerializers(
                clientes['natural'], 
                many=True
            ).data,
            'couriers': GeneralListClientCourierSerializers(
                clientes['courier'], 
                many=True
            ).data
        }
        
        return Response(serialized_data  , status=status.HTTP_200_OK)

    
    def post(self, request, *args, **kwargs):
        #the client should send the attribute to select which model will use de backend
        #the key should be ModelSelected


        #IMPORTANT
        """
            example of information if the user is  a courriertype:

            {
                "nombre": "Empresa Ejemplo S.A.",
                "apellido": "Empresa Ejemplo Apellido",
                "identificacion": "J-123456789",
                "correo": "empresa@example.com",
                "correo_aux": "contacto@example.com",
                "telefono": "+58412567890",
                "telefono_aux": "+58212456789",
                "codigo_cliente": "CLI-2024-001",
                "is_active": true,
                "usuario_destino": {
                    "nombre": "Juan Pérez",
                    "apellido": "Gómez",
                    "identificacion": "V-9876543",
                    "correo": "juan@example.com",
                    "correo_aux": "juan.backup@example.com",
                    "telefono": "+58414654321",
                    "telefono_aux": "+58212345678",
                    "is_active": true
                },
                "direcciones_cliente_courier": [
                    {
                        "estado": "Miranda",
                        "municipio": "Baruta",
                        "sector": "Oficina Principal",
                        "casa": "Torre Empresarial, Piso 10"
                    },
                    {
                        "estado": "Caracas",
                        "municipio": "Libertador",
                        "sector": "Centro",
                        "casa": "Av. Principal, Edificio Central"
                    }
                ],
                "direcciones_destino": [
                    {
                        "estado": "Carabobo",
                        "municipio": "Valencia",
                        "sector": "Zona Industrial",
                        "casa": "Nave 5, Bodega 12"
                    },
                    {
                        "estado": "Aragua",
                        "municipio": "Maracay",
                        "sector": "Zona Norte",
                        "casa": "Calle Comercial, Local 8"
                    }
                ]
            }



            example of information if the user is  a naturaltype:
            {
                "nombre": "María García",
                "apellido": "López",
                "identificacion": "V-12345678",
                "correo": "maria@example.com",
                "correo_aux": "maria.backup@example.com",
                "telefono": "+58412345678",
                "telefono_aux": "+58412345679",
                "codigo_cliente": "CLI-NAT-2023-001",
                "is_active": true,
                "quien_envia": {
                    "nombre": "Carlos Rodríguez",
                    "apellido": "Pérez",
                    "identificacion": "V-87654321",
                    "correo": "carlos@example.com",
                    "correo_aux": "carlos.backup@example.com",
                    "telefono": "+58414444444",
                    "telefono_aux": "+58415555555",
                    "is_active": true
                },
                "quien_recibe": {
                    "nombre": "Ana Martínez",
                    "apellido": "Gómez",
                    "identificacion": "V-55555555",
                    "correo": "ana@example.com",
                    "correo_aux": "ana.backup@example.com",
                    "telefono": "+58416666666",
                    "telefono_aux": "+58417777777",
                    "is_active": true
                },
                "direcciones_cliente_natural": [
                    {
                        "estado": "Miranda",
                        "municipio": "Baruta",
                        "sector": "Urbanización Las Mercedes",
                        "casa": "Calle 1, Edificio A, Piso 3",
                        "is_active": true
                    }
                ],
                "direcciones_quien_envia": [
                    {
                        "estado": "Carabobo",
                        "municipio": "Valencia",
                        "sector": "Zona Industrial",
                        "casa": "Nave 5, Bodega 12",
                        "is_active": true
                    }
                ],
                "direcciones_quien_recibe": [
                    {
                        "estado": "Aragua",
                        "municipio": "Maracay",
                        "sector": "Zona Norte",
                        "casa": "Calle Comercial, Local 8",
                        "is_active": true
                    },
                    {
                        "estado": "Zulia",
                        "municipio": "Maracaibo",
                        "sector": "La Lago",
                        "casa": "Torre 10, Piso 5",
                        "is_active": true
                    }
                ]
            }

                     
        
        """
        
        tipo_cliente = request.headers.get('Tipo-Cliente', "").lower()
        if tipo_cliente not in ['natural', 'courier']:
            return Response(
                {'error': 'Tipo de cliente no válido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            cliente_creado = self.service.crear_cliente(data=request.data,tipo_cliente=tipo_cliente ,request=request)
            return Response(cliente_creado.data,status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )




class GetNaturalOrCourierClient(RetrieveUpdateDestroyAPIView):

    def __init__(self):
        self.service = ClienteService()

    #the client should send the attribute to select which model will use de backend
    #the key should be ModelSelected
    def retrieve(self, request, *args, **kwargs):
        tipo_cliente = self.service.get_tipo_de_cliente(client_type=request.headers.get('Tipo-Cliente', ""))
        if tipo_cliente=="error":
            return Response({'error': 'Tipo de cliente no válido'},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            client = self.service.list_client(id = kwargs["pk"] , tipo_cliente=tipo_cliente)
            return Response(client.data , status=status.HTTP_200_OK)
        except  ValueError as e:  
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )  


    def update(self, request, *args, **kwargs):
        #the client should send the attribute to select which model will use de backend
        #the key should be ModelSelected
        tipo_cliente = self.service.get_tipo_de_cliente(client_type=request.headers.get('Tipo-Cliente', ""))
        if tipo_cliente=="error":
            return Response({'error': 'Tipo de cliente no válido'},status=status.HTTP_400_BAD_REQUEST)

        try:
            cliente =  self.service.update_cliente(id=kwargs["pk"] , tipo_cliente = tipo_cliente  , request=request)
            return Response(cliente.data , status=status.HTTP_200_OK)
        except  ValueError as e:  
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )  
            

            
    def destroy(self, request, *args, **kwargs):
        #the client should send the attribute to select which model will use de backend
        #the key should be ModelSelected

        tipo_cliente = self.service.get_tipo_de_cliente(client_type=request.headers.get('Tipo-Cliente', ""))
        if tipo_cliente == "error":
            return Response({'error': 'Tipo de cliente no válido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if tipo_cliente == "natural":
                client = ClientNatural.objects.get(pk=kwargs["pk"])
            else:
                client = ClientCourier.objects.get(pk=kwargs["pk"])
            
            #client.activate() activate es la vista funcion que me permite activar lo que elimino en la eliminacion logica
            #en el caso de que exista la necesida puedo crear el endponit y activarlos , esa funciones estan en sus respectivos modelos
            client.delete()
            
            return Response(
                {'message': 'Cliente desactivado exitosamente junto con sus relaciones'},
                status=status.HTTP_200_OK
            )
        except (ClientNatural.DoesNotExist, ClientCourier.DoesNotExist):
            return Response(
                {'error': 'Cliente no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error al desactivar el cliente: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        




class ClienteRelacionadoView(RetrieveUpdateAPIView):

    # importante Desplegar
    """
    esta res la informacion que se tiene que enviar en la solicitud para que se pueda 
    seleccionar el mes correcto. cada uno de os casos se les tiene que pasar una informacion
    especifica.


    ClientCourier destino:
    GET /clientes/relacionado/1/
    Header: Tipo-Relacion: destino

    ClientNatural quien_envia:
    GET /clientes/relacionado/1/
    Header: Tipo-Relacion: quien_envia

    ClientNatural quien_recibe:
    GET /clientes/relacionado/1/
    Header: Tipo-Relacion: quien_recibe
    
    """
    
    
    def __init__(self):
        self.service = ClienteRelacionadosService()

    def get_object(self):
        tipo_relacion = self.request.headers.get('Tipo-Relacion', '').lower()
        try:
            return self.service.get_cliente_relacionado(
                pk=self.kwargs['pk'],
                tipo_relacion=tipo_relacion
            )
        except ValueError as e:
            raise ValidationError({'error': str(e)})
        except NotFound as e:
            raise NotFound(str(e))

    def get_serializer_class(self):
        tipo_relacion = self.request.headers.get('Tipo-Relacion', '').lower()
        config = self.service.RELACIONES_CONFIG.get(tipo_relacion, {})
        return config.get('serializer', ClientCourierDestinoSerializer)

    def update(self, request, *args, **kwargs):
        tipo_relacion = request.headers.get('Tipo-Relacion', '').lower()
        try:
            result = self.service.update_cliente_relacionado(
                obj=self.get_object(),
                request_data=request.data,
                tipo_relacion=tipo_relacion
            )
            
            if not result["Success"]:
                return Response(result["data"], status=status.HTTP_400_BAD_REQUEST)
            
            return Response(result["data"], status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )