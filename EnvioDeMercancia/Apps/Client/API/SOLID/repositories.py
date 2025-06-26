from EnvioDeMercancia.Apps.Client.models import (
    ClientNatural,
    ClientCourier
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
    



