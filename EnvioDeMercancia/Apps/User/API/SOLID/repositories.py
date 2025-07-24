from abc import ABC, abstractmethod

#DJANGO
from django.utils import timezone
from django.contrib.sessions.models import Session

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


class RepositorioUsarioLecturaLogout(ABC):
    @abstractmethod
    def get_user(self , model ,  userid ):
        pass

class SessionRepository(ABC):
    @abstractmethod
    def clear_sessions(self, user):
        pass   

 








#this class handle logout querys
class RepositorioSQLogout(RepositorioUsarioLecturaLogout):

    def get_user(self , model , userid):
        try:
            query = model.objects.filter(id = userid).first()
            return query
        except:
            return None
    
class DjangoSessionRepository(SessionRepository):   
    def clear_sessions(self , user):
        all_session = Session.objects.filter(expire_date__gte= timezone.now())
        for session in all_session:
            session_data = session.get_decoded()
            if str(session_data.get('_auth_user_id'))==str(user.first().id ):
                session.delete()
      

#this class handle user querys
class RepositorioSQLUser(RepositorioUsarioEscritura , RepositorioUsarioLectura ):

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
            return {"success":False , "error": str(e)}
     
    def UpdateUserRepositori(self  , modelo ,  pk ):
        try :
            query = modelo.objects.filter(id=pk).first()
            if query is not None:      
                return {"success":True , "result":query}
            return {"success":False , "error": "user not found"}
        except modelo.DoesNotExist:
            return {"success":False , "error": "user not found"}
        except Exception as e:
            return {"success":False , "error": str(e)}
        
    def GetOneUserRepositori(self , modelo ,  pk ):
        try:
            query = modelo.objects.filter(id=pk).first()
            return {"success":True , "result":query}
        except modelo.DoesNotExist:
            return {"success":False , "error": "user not found"}
        except Exception as e:
            return {"success":False , "error": str(e)}
            
    def GetAllUsersRepositori(self , modelo):
        try:
            query = modelo.objects.filter(is_active=True)
            return  query
        except:
            return None

        


