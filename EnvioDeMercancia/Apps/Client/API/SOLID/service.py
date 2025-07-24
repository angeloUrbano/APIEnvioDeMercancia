# from EnvioDeMercancia.Apps.Client.models import (
#     ClientNatural,
#     ClientCourier,
#     ClienteUsuarioDestino,
#     ClienteQuienEnvia,
#     ClienteQuienRecibe,
#     Direccion
# )


from rest_framework.exceptions import NotFound
from rest_framework.exceptions import APIException
from rest_framework import status

from django.core.exceptions import ValidationError



# serializers cliente destino
#from EnvioDeMercancia.Apps.Client.API.serializers.clienteDestinoSerializers import ClientCourierDestinoSerializer , ClientCourierDestinoUpdateSerializer

#serializers cliente quien envia
#from EnvioDeMercancia.Apps.Client.API.serializers.clienteQuienEnviaSerializers  import ClientNaturalQuienEnviaSerializer, ClientNaturalQuienEnviaUpdateSerializer

#serializers cliente quien recibe
# from EnvioDeMercancia.Apps.Client.API.serializers.clienteQuienRecibeSerializers import (
# ClientNaturalQuienRecibeSerializer , ClientNaturalQuienRecibeUpdateSerializer
# )




#serializers client courier , list create and update
#from EnvioDeMercancia.Apps.Client.API.serializers.courierSerializer import GeneralListClientCourierSerializers , ClientCourierCreateSerializer , ClientCourierUpdateSerializer

#serializers client natural , list create and update
# from EnvioDeMercancia.Apps.Client.API.serializers.naturalSerializers import  (GeneralListClienNaturaltSerializers , ClientNaturalCreateSerializer , ClientNaturalUpdateSerializer,
                                                                              
# GeneralListClienNaturaltSerializers2 , ClientNaturalCreateSerializer2,
# ClientNaturalUpdateSerializer2
#                                                                               )




from EnvioDeMercancia.Apps.Client.API.serializers.naturalSerializers import  (
                                                                              
GeneralListClienNaturaltSerializers2 , ClientNaturalCreateSerializer2,
ClientNaturalUpdateSerializer2)



from EnvioDeMercancia.Apps.Client.API.serializers.AuditoriaSerializer.AuditoriaClientSerializer import ClientNaturalHistoricalSerializer




#from EnvioDeMercancia.Apps.Client.API.SOLID.repositories import ClienteRepository , ClienteRepository2 


from EnvioDeMercancia.Apps.Client.API.SOLID.repositories import ClienteRepository2 

from EnvioDeMercancia.Apps.Client.models import ClientNatural2


# from EnvioDeMercancia.Apps.Client.API.serializers.AuditoriaSerializer.AuditoriaClientSerializer import (
# ClientDestinoHistoricalSerializer,
# ClienteQuienEnviaHistoricalSerializer,
# ClienteQuienRecibeHistoricalSerializer,
# ClientNaturalHistoricalSerializer,
# ClientCourierHistoricalSerializer,
# DireccionHistoricalSerializer)




""" 

class ClienteService:
    def __init__(self):
        self.repository = ClienteRepository()

    def list_all_clients(self):
        return{
            "natural" : self.repository.get_all_naturales(),
            "courier": self.repository.get_all_courier()
        }
    

    def crear_cliente(self, data, tipo_cliente , request):
        if tipo_cliente == "natural":
            serializer = ClientNaturalCreateSerializer(data=data , context={"request":request})
        else:
            serializer = ClientCourierCreateSerializer(data=data , context={"request":request})

        if serializer.is_valid():
            serializer.save()
            return serializer
        raise ValueError(serializer.errors)
    
    def update_cliente(self, id, tipo_cliente , request):


        if tipo_cliente == "natural":
            client = self.repository.get_natural(id)
            serializer = ClientNaturalUpdateSerializer(instance=client , data= request.data , context={"request":request})
        else:
            client = self.repository.get_courier(id)
            serializer = ClientCourierUpdateSerializer(instance=client , data= request.data , context={"request":request})

        if serializer.is_valid():
            serializer.save()
            return serializer
        raise ValueError(serializer.errors)


    def list_client(self  , id  , tipo_cliente):
        if tipo_cliente=="natural":
            client = self.repository.get_natural(id)
            serializer =GeneralListClienNaturaltSerializers(client)
        else:
            client = self.repository.get_courier(id)
            serializer =  GeneralListClientCourierSerializers(client)


        return serializer
    

    def get_tipo_de_cliente(self , client_type):
        tipo_cliente = client_type.lower()
        if tipo_cliente not in ['natural', 'courier']:
            return 'error'
        return tipo_cliente
    





"""









#--------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


class CustomAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Ocurrió un error en el servidor'
    default_code = 'error'

    def __init__(self, detail=None, code=None, status_code=None):
        if status_code is not None:
            self.status_code = status_code
        super().__init__(detail=detail, code=code)




class ClienteService2:
    def __init__(self):
        self.repository = ClienteRepository2()

    def list_all_clients(self):

        try:
            all_clients = self.repository.get_all_Clients()
            serializer = GeneralListClienNaturaltSerializers2(all_clients, many=True)
            return serializer.data
        except Exception as e:
            raise CustomAPIException(
                detail=f'Error al listar clientes: {str(e)}',
                status_code=status.HTTP_400_BAD_REQUEST
            )
    

    def create_client(self, data):
        try:
            serializer = ClientNaturalCreateSerializer2(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return serializer.data
        except ValidationError as e:
            raise CustomAPIException(
                detail=e.message_dict if hasattr(e, 'message_dict') else str(e),
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        except Exception as e:
            raise CustomAPIException(
                detail=f'Error al crear cliente: {str(e)}',
                status_code=status.HTTP_400_BAD_REQUEST
            )

    

    
    def update_cliente(self, id, update_data):

        try:

            client = self.repository.get_client(id)
            if not client:
                raise CustomAPIException(
                    detail='Cliente no encontrado',
                    status_code=status.HTTP_404_NOT_FOUND
                )
        
            serializer = ClientNaturalUpdateSerializer2(instance=client , data=update_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return serializer.data
        
        except ValidationError as e:
            raise CustomAPIException(
                detail=e.message_dict if hasattr(e, 'message_dict') else str(e),
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        except Exception as e :
            raise CustomAPIException(
                detail=f'Error al editar cliente: {str(e)}',
                status_code=status.HTTP_400_BAD_REQUEST
            )


    def list_client(self  , id):

        try:
            client = self.repository.get_client(id)
            if not client:
                raise CustomAPIException(
                    detail='Cliente no encontrado',
                    status_code=status.HTTP_404_NOT_FOUND
                )
            serializer =GeneralListClienNaturaltSerializers2(client)
            return serializer.data
        
        except ValidationError as e:
            raise CustomAPIException(
                detail=e.message_dict if hasattr(e, 'message_dict') else str(e),
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        except Exception as e :
            raise CustomAPIException(
                detail=f'Error! user no encontrado: {str(e)}',
                status_code=status.HTTP_400_BAD_REQUEST
            )

    








class AudicotiriaClientsService:
    
    TYPE_MODEL_CONFIG={
        "natural":{
            "model":ClientNatural2,
            "serializer":ClientNaturalHistoricalSerializer,
        }
    }

    @classmethod
    def get_listado_cliente(cls , model_selected):

        config = cls.TYPE_MODEL_CONFIG.get(model_selected)
        if not config:
            raise ValueError('Model seleccionado no valido')

        query = config["model"].historical.model.objects.all()

        serializer  = config["serializer"](query , many=True).data

        return serializer
    


















#--------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>














""" 



class AudicotiriaClientsService:
    
    TYPE_MODEL_CONFIG={

        "courier":{
            "model":ClientCourier,
            "serializer":ClientCourierHistoricalSerializer,
        },
        "natural":{
            "model":ClientNatural,
            "serializer":ClientNaturalHistoricalSerializer,
        },
        "destino":{
            "model":ClienteUsuarioDestino,
            "serializer":ClientDestinoHistoricalSerializer,
        },

        "quien_envia":{
            "model":ClienteQuienEnvia,
            "serializer":ClienteQuienEnviaHistoricalSerializer,
        },

        "quien_recibe":{
            "model":ClienteQuienRecibe,
            "serializer":ClienteQuienRecibeHistoricalSerializer,
        },
          "direccion":{
            "model": Direccion,
            "serializer":DireccionHistoricalSerializer,
        }

    }

    @classmethod
    def get_listado_cliente(cls , model_selected):

        config = cls.TYPE_MODEL_CONFIG.get(model_selected)
        if not config:
            raise ValueError('Model seleccionado no valido')
        
        query = config["model"].historical.model.objects.all()

        serializer  = config["serializer"](query , many=True).data

        return serializer



class ClienteRelacionadosService:

    RELACIONES_CONFIG ={
        "destino":{
            "model":ClientCourier,
            "relacion":"usuario_destino",
            "direcciones": "direcciones_destino",
            "serializer":ClientCourierDestinoSerializer,
            "update_serializer":ClientCourierDestinoUpdateSerializer

        },
        "quien_envia":{
            'model': ClientNatural,
            'relacion': 'quien_envia',
            'direcciones': 'direcciones_quien_envia',
            'serializer': ClientNaturalQuienEnviaSerializer,
            'update_serializer': ClientNaturalQuienEnviaUpdateSerializer
        },
        "quien_recibe":{
            'model': ClientNatural,
            'relacion': 'quien_recibe',
            'direcciones': 'direcciones_quien_recibe',
            'serializer': ClientNaturalQuienRecibeSerializer,
            'update_serializer': ClientNaturalQuienRecibeUpdateSerializer
        }
    }

    def get_cliente_relacionado(self, pk, tipo_relacion):
        config = self.RELACIONES_CONFIG.get(tipo_relacion)
        if not config:
            raise ValueError('Tipo de relación no válido')
        
        queryset = config['model'].objects.select_related(
            config['relacion']
        ).prefetch_related(
            f"{config['relacion']}__{config['direcciones']}"
        )
        
        try:
            return queryset.get(pk=pk)
        except config['model'].DoesNotExist:
            raise NotFound(f"{config['model'].__name__} no encontrado")

    def update_cliente_relacionado(self, obj, request_data, tipo_relacion):
        config = self.RELACIONES_CONFIG.get(tipo_relacion)
        if not config:
            raise ValueError('Tipo de relación no válido')

        serializer = config['update_serializer'](
            instance=obj,
            data=request_data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return {
                "Success": True,
                "data": config['serializer'](obj).data
            }
        return {
            "Success": False,
            "data": serializer.errors
        }




  """          


