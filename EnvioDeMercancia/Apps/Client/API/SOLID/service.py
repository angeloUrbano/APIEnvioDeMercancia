
#serializers client courier , list create and update
from EnvioDeMercancia.Apps.Client.API.serializers.courierSerializer import GeneralListClientCourierSerializers , ClientCourierCreateSerializer , ClientCourierUpdateSerializer

#serializers client natural , list create and update
from EnvioDeMercancia.Apps.Client.API.serializers.naturalSerializers import  GeneralListClienNaturaltSerializers , ClientNaturalCreateSerializer , ClientNaturalUpdateSerializer


from EnvioDeMercancia.Apps.Client.API.SOLID.repositories import ClienteRepository , clientesRelacionadosRepository





# serializers cliente destino
from EnvioDeMercancia.Apps.Client.API.serializers.clienteDestinoSerializers import ClientCourierDestinoSerializer , ClientCourierDestinoUpdateSerializer

#serializers cliente quien envia
from EnvioDeMercancia.Apps.Client.API.serializers.clienteQuienEnviaSerializers  import ClientNaturalQuienEnviaSerializer, ClientNaturalQuienEnviaUpdateSerializer

#serializers cliente quien recibe
from EnvioDeMercancia.Apps.Client.API.serializers.clienteQuienRecibeSerializers import (
ClientNaturalQuienRecibeSerializer , ClientNaturalQuienRecibeUpdateSerializer
)

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

    def __init__(self):
        self.repository = clientesRelacionadosRepository()

    def update_client_Relacionado(self , obj  , request , serializer_a_usar):
        serializer = serializer_a_usar( obj  , data = request)
        if serializer.is_valid():
            serializer.save()
            return {"Success":True , "data": serializer.data }
        else:
            return {"Success":False , "data": serializer.errors}






            


