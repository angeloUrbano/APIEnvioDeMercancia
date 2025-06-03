from rest_framework import  viewsets
from rest_framework import status
from rest_framework.response import Response


from EnvioDeMercancia.Apps.User.models import User
from EnvioDeMercancia.Apps.User.API.serializers.serializersUser import userSerilizer

from EnvioDeMercancia.Apps.User.API.SOLID.repositories import RepositorioSQL
from EnvioDeMercancia.Apps.User.API.SOLID.services import GestionUserSerializersService


#users crud 
class UsersCrudViewSet(viewsets.ModelViewSet):
    serializer_class = userSerilizer
    queryset =  serializer_class.Meta.model.objects.all()
    #querysRepositorioSQL = RepositorioSQL()
    #gestionService = GestionUserSerializersService()
    modelo = User


    def __init__(self, repository=None, service=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.querysRepositorioSQL = repository or RepositorioSQL()
        self.gestionService = service or GestionUserSerializersService()

    """
    data to create an user
    {
        "username": "prueba",
        "name": "prueba",
        "last_name": "prueba",
        "email": "prueba@gmail.com",
        "password": "prueba"
    }
    
    """

    #GET ALL USERS
    def list(self  , request):
        try:
            query = self.querysRepositorioSQL.GetAllUsersRepositori(self.modelo)
            user_serializers = self.gestionService.GetAllUsersService(self.serializer_class , query)
            return Response(user_serializers , status= status.HTTP_200_OK)
        except:
            return Response({"message":"server error"} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # create users
    def create(self , request):
  
        userCreated =  self.gestionService.SaveUsersService(self.serializer_class ,  request.data)
        if userCreated["success"]:
           return Response(userCreated["info"], status = status.HTTP_201_CREATED)
        
        elif userCreated["success"]==False and "infoFormulario" in userCreated:
            return Response({userCreated["info"] } , status= status.HTTP_400_BAD_REQUEST)
        else:
            return Response(userCreated["infoServidor"], status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #delete user  
    def destroy(self , request , pk=None):
        userDeleted =  self.querysRepositorioSQL.DeleteUserRepositori(self.modelo , pk)
        if  userDeleted["success"] ==False :
            return Response({"message":"server error" , "error":userDeleted["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        elif userDeleted["success"]:
            #eliminado
            return Response({"message":"user deleted"} , status= status.HTTP_200_OK)
        
    #update user
    def update(self , request , pk=None): 
        query = self.querysRepositorioSQL.UpdateUserRepositori(self.modelo , pk)
        if  query["success"] ==False :
            return Response({"message":"server error" , "error":query["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        user_serializer = self.gestionService.UpdateUserService(self.serializer_class ,  query["result"] , request.data) 
        # in case user not found etc
       
        #editando
        if user_serializer["success"]:
            return Response(user_serializer["info"] , status=status.HTTP_200_OK)
        #error en la consulta , etc
        elif user_serializer["success"]==False and "infoFormulario" in user_serializer :
            return Response(user_serializer["infoFormulario"], status= status.HTTP_400_BAD_REQUEST)
        #error servidor
        else:
            return Response(user_serializer["infoServidor"], status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
    #this function get just one user
    def retrieve (self , request , pk=None):
        query = self.querysRepositorioSQL.GetOneUserRepositori(self.modelo , pk)
        # in case user not found etc
        if  query["success"] ==False :
            return Response({"message":"server error" , "error":query["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        user_serializer =  self.gestionService.GetOneUserService(self.serializer_class , query["result"] )
        
        if user_serializer["success"]:
            return Response(user_serializer["info"] , status=status.HTTP_200_OK)
        #error en la consulta , etc
        elif user_serializer["success"]==False and "infoFormulario" in user_serializer :
            return Response(user_serializer["info"], status=status.HTTP_404_NOT_FOUND)
        #error servidor
        else:
            return Response(user_serializer["infoServidor"], status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        


        





