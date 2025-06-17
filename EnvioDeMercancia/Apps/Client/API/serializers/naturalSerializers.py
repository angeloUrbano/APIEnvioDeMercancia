
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

from EnvioDeMercancia.Apps.Client.API.serializers.direccionesSerializers import DireccionSerializer ,DireccionSerializerEditar




#list Client Natural ---------------------------------------->>>>>>>>>>>>>>>>>>>>>>>


# Model ClienteUsuarioDestino
class allClientRelatedToClientNaturalFromClientQuienEnviaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClienteQuienEnvia
        fields = "__all__"

# Model ClienteUsuarioDestino
class allClientRelatedToClientNaturalFromClientQuienRecibeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClienteQuienRecibe
        fields = "__all__"



class GeneralListClienNaturaltSerializers(serializers.ModelSerializer):
    quien_envia = allClientRelatedToClientNaturalFromClientQuienEnviaSerializer(read_only=True)# attributes Serializer  , whith this way a achive get all attributes joined
    quien_recibe = allClientRelatedToClientNaturalFromClientQuienRecibeSerializer(read_only=True)# attributes Serializer  , whith this way a achive get all attributes joined
    direcciones_cliente_natural = serializers.SerializerMethodField()
    direcciones_quien_envia = serializers.SerializerMethodField()
    direcciones_quien_recibe = serializers.SerializerMethodField()

    class Meta:
        model = ClientNatural
        fields = "__all__"

    def get_direcciones_cliente_natural(self, obj):
        return DireccionSerializer(obj.direcciones_cliente_natural.all(), many=True).data

    def get_direcciones_quien_envia(self, obj):
        return DireccionSerializer(obj.quien_envia.direcciones_quien_envia.all(), many=True).data

    def get_direcciones_quien_recibe(self, obj):
        return DireccionSerializer(obj.quien_recibe.direcciones_quien_recibe.all(), many=True).data
    

#serializer to save courierNatrural and ClienteQuienEnvia and ClienteQuienRecibe
class ClientNaturalCreateSerializer(serializers.ModelSerializer):
    quien_envia = allClientRelatedToClientNaturalFromClientQuienEnviaSerializer()# attributes Serializer  , whith this way a achive get all attributes joined
    quien_recibe = allClientRelatedToClientNaturalFromClientQuienRecibeSerializer()# attributes Serializer  , whith this way a achive get all attributes joined
    direcciones_cliente_natural = DireccionSerializer(many=True)# attributes Serializer  , whith this way a achive get all attributes joined

    # la explicacion de porque uso serializers.SerializerMethodField() esta en el modelo ClientCourierCreateSerializer
    direcciones_quien_envia =  serializers.SerializerMethodField()
    direcciones_quien_recibe = serializers.SerializerMethodField()


    class Meta:
        model= ClientNatural
        fields = "__all__"

    #la explicacion de estos dos metodos estra en el modelo ClientCourierCreateSerializer
    def get_direcciones_quien_recibe(self , obj):
        return DireccionSerializer(obj.quien_envia.direcciones_quien_envia.all() , many=True).data

    def get_direcciones_quien_envia(self , obj):
        return DireccionSerializer(obj.quien_recibe.direcciones_quien_recibe.all() , many=True).data
    

    @transaction.atomic
    def create(self , validated_data):
        usuario_quien_envia_data = validated_data.pop("quien_envia")
        usuario_quien_recibe_data = validated_data.pop("quien_recibe")
        direcciones_cliente_natural_data = validated_data.pop("direcciones_cliente_natural" , [])

        # por que uso esto self.context["request"].data.ge y no  se explica en el modelo ClientCourierCreateSerializer
        direcciones_cliente_quien_envia_data =self.context["request"].data.get("direcciones_quien_envia" , [])
        direcciones_cliente_quien_recibe_data = self.context["request"].data.get("direcciones_quien_recibe" , [])



        try:
            usuario_quien_envia = ClienteQuienEnvia.objects.create(**usuario_quien_envia_data)
        except IntegrityError as e:
            raise serializers.ValidationError({"quien_envia": " error creando usuario destino. El error puede ser causado debido a que el correo o identificación ya existe."})
        
        try:
            usuario_quien_recibe = ClienteQuienRecibe.objects.create(**usuario_quien_recibe_data)
        except IntegrityError as e:
            raise serializers.ValidationError({"quien_recibe": " error creando usuario destino. El error puede ser causado debido a que el correo o identificación ya existe."})



        usuario_Natural = ClientNatural.objects.create(
            quien_envia = usuario_quien_envia,
            quien_recibe = usuario_quien_recibe,
            **validated_data

        )

        # en caso que no vengan direcciones de cliente natural
        if not direcciones_cliente_natural_data:
            raise ValidationError("Debe proporcionar al menos una dirección para el cliente natural.")
        for direccion_data in direcciones_cliente_natural_data:
            Direccion.objects.create(
                cliente_natural=usuario_Natural,
                **direccion_data
        )


        # en caso que no vengan direcciones de quien envia 
        if not direcciones_cliente_quien_envia_data:
            raise ValidationError("Debe proporcionar al menos una dirección para el cliente que envia.")
        for direccion_data in direcciones_cliente_quien_envia_data:
            Direccion.objects.create(
                cliente_quien_envia=usuario_quien_envia,
                **direccion_data
        )

        # en caso que no vengan direcciones de quien recibe 
        if not direcciones_cliente_quien_recibe_data:
                    raise ValidationError("Debe proporcionar al menos una dirección para el cliente que recibe.")   
        for direccion_data in direcciones_cliente_quien_recibe_data:
            Direccion.objects.create(
                cliente_quien_recibe=usuario_quien_recibe ,
                **direccion_data
        )




        return usuario_Natural
    

# serializer update natural client
class ClientNaturalUpdateSerializer(serializers.ModelSerializer):
    direcciones_cliente_natural = DireccionSerializerEditar(many=True, required=False , read_only=False)

    class Meta:
        model = ClientNatural
        fields = [
            'nombre',
            'apellido',
            'identificacion',
            'correo',
            'correo_aux',
            'telefono',
            'telefono_aux',
            'codigo_cliente',
            'is_active',
            'direcciones_cliente_natural'
        ]
        extra_kwargs = {
            'identificacion': {'validators': []},  # Desactiva validadores automáticos
            'correo': {'validators': []},
            'correo_aux': {'validators': []}
        }

    def update(self, instance, validated_data):
        direcciones_data = validated_data.pop("direcciones_cliente_natural", None)
        
        # Validación manual de campos únicos
        self._validate_unique_fields(instance, validated_data)
        
        cliente = super().update(instance, validated_data)

        if direcciones_data is not None:
            self._update_direcciones(instance, direcciones_data)

        return cliente
    
    def _validate_unique_fields(self, instance, validated_data):
        errors = {}
        
        # Validar identificación
        identificacion = validated_data.get('identificacion', instance.identificacion)
        if ClientNatural.objects.exclude(pk=instance.pk).filter(identificacion=identificacion).exists():
            errors['identificacion'] = ["Esta identificación ya está en uso"]
        
        # Validar correo
        correo = validated_data.get('correo', instance.correo)
        if ClientNatural.objects.exclude(pk=instance.pk).filter(correo=correo).exists():
            errors['correo'] = ["Este correo ya está en uso"]
        
        # Validar correo auxiliar
        correo_aux = validated_data.get('correo_aux', instance.correo_aux)
        if correo_aux and ClientNatural.objects.exclude(pk=instance.pk).filter(correo_aux=correo_aux).exists():
            errors['correo_aux'] = ["Este correo auxiliar ya está en uso"]
        
        if errors:
            raise serializers.ValidationError(errors)

    def _update_direcciones(self, instance, direcciones_data):
        for dir_data in direcciones_data:
            if 'id' in dir_data:
                Direccion.objects.filter(
                    id=dir_data['id'],
                    cliente_natural=instance
                ).update(
                    estado=dir_data.get('estado'),
                    municipio=dir_data.get('municipio'),
                    sector=dir_data.get('sector'),
                    casa=dir_data.get('casa'),
                    is_active=dir_data.get('is_active', True)
                )
   