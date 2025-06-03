from abc import ABC, abstractmethod

"""
    Acceso a los datos

"""
class RepositorioUsarioEscritura(ABC):

    @abstractmethod
    def UpdateUserRepositori(self , user_id):
        pass
    @abstractmethod
    def DeleteUserRepositori(self  , serializerClass ,  pk):
        pass

class RepositorioUsarioLectura(ABC):
    @abstractmethod
    def GetAllUsersRepositori(self , allUsers):
        pass
    @abstractmethod
    def GetOneUserRepositori(self , serializerClass ,  pk ):
        pass


class RepositorioSQL(RepositorioUsarioEscritura , RepositorioUsarioLectura ):

    def DeleteUserRepositori(self  , modelo ,  pk):
        try:
            query = modelo.objects.filter(id=pk).first()
            if query:
                query.is_active=False
                query.save()
                return{"success":True}        
        except modelo.DoesNotExist:
            return {"success":False , "error": "user not found"}
        except Exception as e:
            return {"success":False , "error": e}
     
    def UpdateUserRepositori(self  , modelo ,  pk ):
        try :
            query = modelo.objects.filter(id=pk).first()      
            return {"success":True , "result":query}
        except modelo.DoesNotExist:
            return {"success":False , "error": "user not found"}
        except Exception as e:
            return {"success":False , "error": e}
        
    def GetOneUserRepositori(self , modelo ,  pk ):
        try:
            query = modelo.objects.filter(id=pk).first()
            return {"success":True , "result":query}
        except modelo.DoesNotExist:
            return {"success":False , "error": "user not found"}
        except Exception as e:
            return {"success":False , "error": e}
            
    def GetAllUsersRepositori(self , modelo):
        try:
            query = modelo.objects.filter(is_active=True)
            return  query
        except:
            return None

        


