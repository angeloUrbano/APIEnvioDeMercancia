from abc import ABC, abstractmethod

from EnvioDeMercancia.Apps.RecepcionEnPuerta.models import CajasAlmacenadas



class RecepcionLecturaRepository(ABC):

    @abstractmethod
    def get_all_box():
        pass

    @abstractmethod
    def get_one_box():
        pass



class RecepcionEscrituraRepository(ABC):

    @abstractmethod
    def create_box():
        pass

    @abstractmethod
    def update_box():
        pass



class RecepcionRepository(RecepcionLecturaRepository):

    def get_all_box(self ):
        try:
            query = CajasAlmacenadas.objects.all()
            return {"success":True , "info":query}
        except Exception as e :
            return {"success":False , "info":str(e)}
        
    def get_one_box(self , pk):
        try:
            query = CajasAlmacenadas.objects.get(id=pk)
            return {"success":True , "info":query}
        except Exception  as e:
            return {"success":False , "info":str(e)}
        

        


