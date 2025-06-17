from rest_framework.exceptions import NotFound


from EnvioDeMercancia.Apps.Client.models import (
    ClienteUsuarioDestino, 
    ClienteQuienEnvia,
    ClienteQuienRecibe, 
    ClientNatural,
    ClientCourier,
    Direccion
)




class ClienteRepository :

    @staticmethod
    def get_all_naturales():
        return ClientNatural.objects.all() 
    
    @staticmethod
    def get_all_courier():
        return ClientCourier.objects.all()
    
    @staticmethod
    def create_natural(data):
        return ClientNatural.objects.create(**data)
    
    @staticmethod
    def create_courier(data):
        return ClientCourier.objects.create(**data)
    

    @staticmethod
    def get_natural(data):
        return ClientNatural.objects.filter(id=data).first()
    
    @staticmethod
    def get_courier(data):
        return ClientCourier.objects.filter(id=data).first()
    



class clientesRelacionadosRepository:

    @staticmethod
    def get_cliente_destino(pk):
        clients =  ClientCourier.objects.all()

        try:
            return clients.select_related(
            'usuario_destino'
            ).prefetch_related(
            'usuario_destino__direcciones_destino'
        ).get(id=pk)
        except ClientCourier.DoesNotExist:
            raise NotFound("ClientCourier no encontrado")
        


    @staticmethod
    def get_cliente_destino(pk):
        clients =  ClientCourier.objects.all()

        try:
            return clients.select_related(
            'usuario_destino'
            ).prefetch_related(
            'usuario_destino__direcciones_destino'
        ).get(id=pk)
        except ClientCourier.DoesNotExist:
            raise NotFound("ClientCourier no encontrado")
        



    
    @staticmethod
    def get_cliente_destino(pk):
        clients =  ClientCourier.objects.all()

        try:
            return clients.select_related(
            'usuario_destino'
            ).prefetch_related(
            'usuario_destino__direcciones_destino'
        ).get(id=pk)
        except ClientCourier.DoesNotExist:
            raise NotFound("ClientCourier no encontrado")