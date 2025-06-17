
from rest_framework import serializers

#django
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.db import transaction


from EnvioDeMercancia.Apps.Client.models import (
    ClienteUsuarioDestino, 
    ClienteQuienEnvia,
    ClienteQuienRecibe, 
    ClientNatural,
    ClientCourier,
    Direccion
)




# directions models ------------------------------------------->>>>>>>>>>>>>>>>>>

# general de direcctiones
class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Direccion
        fields = "__all__"
        extra_kwargs = {
            'cliente_natural': {'required': False},
            'cliente_courier': {'required': False},
            'cliente_quien_envia': {'required': False},
            'cliente_quien_recibe': {'required': False},
            'cliente_destino': {'required': False},
        }




#porque para editar necesito el id
class DireccionSerializerEditar(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = "__all__"
        extra_kwargs = {
            'id': {'read_only': False},  # Esto es clave
            'cliente_natural': {'required': False, 'write_only': True},
            'cliente_courier': {'required': False, 'write_only': True},
            'cliente_quien_envia': {'required': False, 'write_only': True},
            'cliente_quien_recibe': {'required': False, 'write_only': True},
            'cliente_destino': {'required': False, 'write_only': True}
        }



