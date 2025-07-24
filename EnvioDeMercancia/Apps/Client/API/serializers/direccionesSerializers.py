
from rest_framework import serializers

#django
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.db import transaction


from EnvioDeMercancia.Apps.Client.models import (

    Direccion2
)




# directions models ------------------------------------------->>>>>>>>>>>>>>>>>>

# general de direcctiones
class DireccionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)# Hacemos el id opcional
    class Meta:
        model=Direccion2
        fields = "__all__"
        extra_kwargs = {
            #'id': {'read_only': False},  # Esto es clave
            'cliente_natural': {'required': False},
            'Agente': {'required': False},
            
        }




#porque para editar necesito el id
class DireccionSerializerEditar(serializers.ModelSerializer):
    class Meta:
        model = Direccion2
        fields = "__all__"
        extra_kwargs = {
            'id': {'read_only': False},  # Esto es clave
            'cliente_natural': {'required': False, 'write_only': True},
            'Agente': {'required': False, 'write_only': True},

        }



