from abc import ABC, abstractmethod

"""
Logica de negocios

"""


class ServiceUsarioEscritura():

    @abstractmethod
    def SaveUsersService(self , serializerClass ,  usuario):
        pass
    @abstractmethod
    def UpdateUserService(self , user_id):
        pass

class ServiceUsarioLectura():
    @abstractmethod
    def SaveUsersService(self , serializerClass ,  usuario):
        pass
    @abstractmethod
    def UpdateUserService(self , user_id):
        pass
    @abstractmethod
    def DeleteUserService(self  , serializerClass ,  pk):
        pass


class GestionUserSerializersService(ServiceUsarioLectura , ServiceUsarioEscritura):
    
    def SaveUsersService(self , serializerClass , requestData):
        try:
            serializer  = serializerClass(data = requestData)
            if serializer.is_valid():
                serializer.save()
                return {"success":True , "info":serializer.data}
            return {"success":False , "infoFormulario":serializer.errors}
        except Exception as e:
            return {"success":False , "infoServidor":e}

    def UpdateUserService(self  , serializerClass , user , requestData):
        try :
            serializer = serializerClass(user  , data = requestData)
            if serializer.is_valid():
                serializer.save()
                return{"success":True , "info":serializer.data }
            return{"success":False , "infoFormulario":serializer.errors} 
        except Exception as e:
            return{"success":False , "infoServidor":e} 
        
    def GetOneUserService(self , serializerClass , user):
        try:
            if user:
                return{"success":True , "info":serializerClass(user).data}
            return{"success":False , "infoFormulario":serializerClass(user).errors} 
        except Exception as e:
            return{"success":False , "infoServidor":e} 

    def GetAllUsersService(self , serializer_class , users):
        allUsers = serializer_class(users, many=True)
        return  allUsers.data


