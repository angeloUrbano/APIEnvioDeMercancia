from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from EnvioDeMercancia.Apps.User.models import User
from django.contrib.auth.models import Group

from django.core.exceptions import ValidationError
from django.db import transaction


from EnvioDeMercancia.Apps.Client.API.serializers.direccionesSerializers import DireccionSerializer , DireccionSerializerEditar

from EnvioDeMercancia.Apps.Client.models import Direccion2
class CustomTokenObtainPairSerilizer(TokenObtainPairSerializer):
    pass



class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields = ["id" , "name"]

        extra_kwargs={
            "name":{"read_only":True},
        }





class userSerilizer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Group.objects.all(),
        required=True
    )
    password = serializers.CharField(write_only=True, required=True)
    direcciones_Agente_or_user =  DireccionSerializer(many=True,  write_only =True, required=True)

    class Meta:
        model = User 
        fields = [
            "username", "email", "name", "second_name", 
            "last_name", "secound_last_name", "password", "codigo_cliente" ,"groups" , "direcciones_Agente_or_user"
        ]



    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['groups'] = GroupsSerializer(instance.groups.all(), many=True).data
        if 'direcciones_Agente_or_user' not in representation:
            representation['direcciones_Agente_or_user'] = DireccionSerializer(
                instance.user.all(), many=True
            ).data
        return representation
    



class userSerilizerCreate(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Group.objects.all(),
        required=True
    )
    password = serializers.CharField(write_only=True, required=True)
    direcciones_Agente_or_user =  DireccionSerializer(many=True,  write_only =True, required=True)
    

    class Meta:
        model = User 
        fields = [
            "username", "email", "name", "second_name", 
            "last_name", "secound_last_name", "password" , "codigo_cliente" ,  "groups" , "direcciones_Agente_or_user"
        ]
        extra_kwargs={
            "name":{"required":True},
            "last_name":{"required":True}
        }
    @transaction.atomic
    def create(self, validated_data):
        groups = validated_data.pop('groups')
        password = validated_data.pop('password')
        direccion  = validated_data.pop("direcciones_Agente_or_user" , [])


        if not direccion or len(direccion)==0 :
            raise ValidationError("Debe proporcionar al menos una dirección para el Usuario")
        
        if not groups :
            raise ValidationError("Debe proporcionar rol de usuario")
        

        #if validated_data["name"]==None or validated_data[""]==None:
 
        # if groups[0].name =="Agente":
        #     if "codigo_cliente" not in validated_data or validated_data["codigo_cliente"]==None: 
        #         raise ValidationError({"error":"debe haber un codigo de cliente que se debe crear en el backend , opcional estoy mandando este mensaje."})
            


        user = User(**validated_data)
        user.set_password(password)
        user.save()

        for direccion_data in direccion:
            Direccion2.objects.create(
                user=user,
                **direccion_data
        )
        

        #Asignar grupos existentes
        user.groups.set(groups)
        
        return user
    @transaction.atomic
    def update(self, instance, validated_data):
        groups = validated_data.pop('groups', None)
        password = validated_data.pop('password', None)
        direcciones_data = validated_data.pop("direcciones_Agente_or_user" , [])

        
        instance = super().update(instance, validated_data)
        
        if password:
            instance.set_password(password)
        
        if groups is not None:
            instance.groups.set(groups)
        

        if direcciones_data is not None:
            self._update_direcciones(instance, direcciones_data)
        
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['groups'] = GroupsSerializer(instance.groups.all(), many=True).data
        if 'direcciones_Agente_or_user' not in representation:
            representation['direcciones_Agente_or_user'] = DireccionSerializer(
                instance.user.all(), many=True
            ).data
        return representation
    
    def _update_direcciones(self, instance, direcciones_data):


        for dir_data in direcciones_data:
            if 'id' in dir_data:  # Ahora el ID estará presente
                Direccion2.objects.filter(
                    id=dir_data['id'],
                    user=instance
                ).update(
                    estado=dir_data.get('estado'),
                    municipio=dir_data.get('municipio'),
                    sector=dir_data.get('sector'),
                    casa=dir_data.get('casa'),
                    pais=dir_data.get('pais'),
                    codigo_postal=dir_data.get('codigo_postal'),
                    is_active=dir_data.get('is_active', True)
                )
    




class userSerilizerUpdate(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Group.objects.all(),
        required=False
    )
    password = serializers.CharField(write_only=True, required=False)
    direcciones_Agente_or_user =  DireccionSerializer(many=True,  write_only =True, required=False)
    

    class Meta:
        model = User 
        fields = [
            "username", "email", "name", "second_name", 
            "last_name", "secound_last_name", "password", "groups" , "direcciones_Agente_or_user"
        ]
   
    @transaction.atomic
    def update(self, instance, validated_data):
        groups = validated_data.pop('groups', None)
        password = validated_data.pop('password', None)
        direcciones_data = validated_data.pop("direcciones_Agente_or_user" , [])



        # if groups[0].name =="Agente":
        #     "se debe validar algo aqui que aun no tengo claro"

        #     print(groups[0].name , "nombre del grupo selected es Agente")
        #     raise ValidationError("Debe proporcionar rol de usuario")

        
        instance = super().update(instance, validated_data)
        
        if password:
            instance.set_password(password)
        
        if groups is not None:
            instance.groups.set(groups)
        

        if direcciones_data is not None:
            print("si se esta intentando editar el usuario")
            self._update_direcciones(instance, direcciones_data)
        
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['groups'] = GroupsSerializer(instance.groups.all(), many=True).data
        if 'direcciones_Agente_or_user' not in representation:
            representation['direcciones_Agente_or_user'] = DireccionSerializer(
                instance.user.all(), many=True
            ).data
        return representation
    
    def _update_direcciones(self, instance, direcciones_data):

        
        for dir_data in direcciones_data:
            if 'id' in dir_data:  # Ahora el ID estará presente
                Direccion2.objects.filter(
                    id=dir_data['id'],
                    user=instance
                ).update(
                    estado=dir_data.get('estado'),
                    municipio=dir_data.get('municipio'),
                    sector=dir_data.get('sector'),
                    casa=dir_data.get('casa'),
                    pais=dir_data.get('pais'),
                    codigo_postal=dir_data.get('codigo_postal'),
                    is_active=dir_data.get('is_active', True)
                )