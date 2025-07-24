
#DRF
from rest_framework import  viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken

#DJANGO
from django.contrib.auth import authenticate
from django.contrib.sessions.models import Session
from django.utils import timezone


#PROPIAS
from EnvioDeMercancia.Apps.User.models import User
from EnvioDeMercancia.Apps.User.API.serializers.serializersUser import (userSerilizer ,CustomTokenObtainPairSerilizer,
userSerilizerUpdate , userSerilizerCreate)
from EnvioDeMercancia.Apps.User.API.SOLID.repositories import RepositorioSQLUser , RepositorioSQLogout , DjangoSessionRepository
from EnvioDeMercancia.Apps.User.API.SOLID.services import GestionUserSerializersService , TokenService , LogoutService


#users crud 
class UsersCrudViewSet(viewsets.ModelViewSet):
    serializer_class = userSerilizer
    queryset = serializer_class.Meta.model.objects.all()
    modelo = User


    def __init__(self, repository=None, service=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.querysRepositorioSQLUser = repository or RepositorioSQLUser()
        self.gestionService = service or GestionUserSerializersService()

    # DESPLEGAR IMPORTANTE
    """
    data to create an user
        second_name es opcional
        second_last_name es opcional
    {
            "username": "nuevousuario",
            "name": "Juannnn",
            "last_name": "Pérez",
            "email": "juan@example.com",
            "password": "contraseña123",
            "codigo_cliente": "pruebaCodigocLIENTE123-321",
            "groups": [
                1
            ],
            "direcciones_Agente_or_user": [
                {
                    "estado": "Miranda",
                    "municipio": "Baruta",
                    "sector": "Oficina Principal",
                    "casa": "Torre Empresarial, Piso 10",
                    "pais":"venezuela",
                    "codigo_postal":"0102"
                },
                {
                "estado": "Caracas",
                "municipio": "Libertador",
                "sector": "Centro",
                "casa": "Av. Principal, Edificio Central",
                "pais":"venezuela",
                "codigo_postal":"0102"
                }
            ]
        }
    
    """

    #GET ALL USERS
    def list(self  , request):
        try:
            query = self.querysRepositorioSQLUser.GetAllUsersRepositori(self.modelo)
            user_serializers = self.gestionService.GetAllUsersService(userSerilizer , query)
            return Response(user_serializers , status= status.HTTP_200_OK)
        except:
            return Response({"message":"server error"} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # create users
    def create(self , request):
  
        userCreated =  self.gestionService.SaveUsersService(userSerilizerCreate ,  request.data)

        if 'infoServidor' in  userCreated:
            return Response(userCreated['infoServidor'] , status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if userCreated["success"]:
           return Response(userCreated["info"], status = status.HTTP_201_CREATED)

        elif userCreated["success"]==False and "infoFormulario" in userCreated:
            return Response(userCreated["infoFormulario"]  , status= status.HTTP_400_BAD_REQUEST)
       
    #delete user  
    def destroy(self , request , pk=None):
        userDeleted =  self.querysRepositorioSQLUser.DeleteUserRepositori(self.modelo , pk)
        if  userDeleted["success"] ==False :
            return Response({"message":"server error" , "error":userDeleted["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        elif userDeleted["success"]:
            #eliminado
            return Response({"message":"user deleted"} , status= status.HTTP_200_OK)
        
    #update user
    def update(self , request , pk=None): 
        query = self.querysRepositorioSQLUser.UpdateUserRepositori(self.modelo , pk)

        if  query["success"] ==False :
            return Response({"message":"server error" , "error":query["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        user_serializer = self.gestionService.UpdateUserService(userSerilizerUpdate ,  query["result"] , request.data) 
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
        query = self.querysRepositorioSQLUser.GetOneUserRepositori(self.modelo , pk)
        # in case user not found etc
        if  query["success"] ==False :
            return Response({"message":"server error" , "error":query["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        user_serializer =  self.gestionService.GetOneUserService(userSerilizer , query["result"] )
        
        if user_serializer["success"]:
            return Response(user_serializer["info"] , status=status.HTTP_200_OK)
        #error en la consulta , etc
        elif user_serializer["success"]==False and "infoFormulario" in user_serializer :
            return Response({"message":"user not found"}, status=status.HTTP_404_NOT_FOUND)
        #error servidor
        else:
            return Response(user_serializer["infoServidor"], status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        
#login class to users system
class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerilizer()

    def post(self , request , *args , **kwargs):
        username = request.data.get("username" , "")
        password = request.data.get("password" , "")
        user =  authenticate(username=username,password=password)
        if not user:
            return Response({"menssage": "user or password incorrect"} , status = status.HTTP_400_BAD_REQUEST)

        tokens = TokenService.generate_token(user)
        user_serializer = userSerilizer(user)
        return Response({
            "Token": tokens["access"],
            "refresh-token":tokens["refresh"],
            "user":user_serializer.data,
            "message":"success"
            } , status = status.HTTP_200_OK)



# users Logout class 
class Logout(GenericAPIView):
    model = User
    userLogoutRepositorie = RepositorioSQLogout()
    logoutService = LogoutService()
    sessionLogout = DjangoSessionRepository()

    def post(self , request , *args , **kwargs):
        user = self.userLogoutRepositorie.get_user(self.model , request.data.get("user"))
        if user is None:
            return Response({"menssage": "user does not exist"} , status = status.HTTP_400_BAD_REQUEST)
        
        self.logoutService.invalidateRefreshToken(user)# invalidate refresh token
        self.sessionLogout.clear_sessions(user) #delete sessions-->
        return Response({"message": "session close correctly"} , status = status.HTTP_200_OK)
        
        
        






