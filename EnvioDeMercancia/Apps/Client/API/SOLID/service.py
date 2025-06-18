from EnvioDeMercancia.Apps.Client.models import (
    ClienteUsuarioDestino, 
    ClienteQuienEnvia,
    ClienteQuienRecibe, 
    ClientNatural,
    ClientCourier,
    Direccion
)

from rest_framework.exceptions import NotFound


# serializers cliente destino
from EnvioDeMercancia.Apps.Client.API.serializers.clienteDestinoSerializers import ClientCourierDestinoSerializer , ClientCourierDestinoUpdateSerializer

#serializers cliente quien envia
from EnvioDeMercancia.Apps.Client.API.serializers.clienteQuienEnviaSerializers  import ClientNaturalQuienEnviaSerializer, ClientNaturalQuienEnviaUpdateSerializer

#serializers cliente quien recibe
from EnvioDeMercancia.Apps.Client.API.serializers.clienteQuienRecibeSerializers import (
ClientNaturalQuienRecibeSerializer , ClientNaturalQuienRecibeUpdateSerializer
)




#serializers client courier , list create and update
from EnvioDeMercancia.Apps.Client.API.serializers.courierSerializer import GeneralListClientCourierSerializers , ClientCourierCreateSerializer , ClientCourierUpdateSerializer

#serializers client natural , list create and update
from EnvioDeMercancia.Apps.Client.API.serializers.naturalSerializers import  GeneralListClienNaturaltSerializers , ClientNaturalCreateSerializer , ClientNaturalUpdateSerializer


from EnvioDeMercancia.Apps.Client.API.SOLID.repositories import ClienteRepository 


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
            serializer = ClientNaturalUpdateSerializer(instance=client , data= request.data)
        else:
            client = self.repository.get_courier(id)
            serializer = ClientCourierUpdateSerializer(instance=client , data= request.data)

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




            


