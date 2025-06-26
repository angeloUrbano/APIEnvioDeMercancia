from rest_framework import serializers

#django
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.db import transaction


from EnvioDeMercancia.Apps.Client.models import (
    ClienteUsuarioDestino, 
    ClientCourier,
    Direccion
)


from EnvioDeMercancia.Apps.Client.API.serializers.direccionesSerializers import DireccionSerializer ,DireccionSerializerEditar




#list Client Courier------------------------------>>>>>>>>>>>>>>>>>>>>>>>>>>

# model ClienteUsuarioDestino
class allClientRelatedToClientCourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClienteUsuarioDestino
        fields = "__all__"

class GeneralListClientCourierSerializers(serializers.ModelSerializer):
    usuario_destino = allClientRelatedToClientCourierSerializer(read_only=True)# attributes Serializer  , whith this way a achive get all attributes joined
    direcciones_cliente_courier = serializers.SerializerMethodField()
    direcciones_destino = serializers.SerializerMethodField()
    
    class Meta:
        model = ClientCourier
        fields = "__all__"

    def get_direcciones_cliente_courier(self, obj):
        return DireccionSerializer(obj.direcciones_cliente_courier.all(), many=True).data

    def get_direcciones_destino(self, obj):
        return DireccionSerializer(obj.usuario_destino.direcciones_destino.all(), many=True).data


#serializer to save courierClient and destinoClient
class ClientCourierCreateSerializer(serializers.ModelSerializer):
    usuario_destino = allClientRelatedToClientCourierSerializer()  # attributes Serializer  , whith this way a achive get all attributes joined
    direcciones_cliente_courier = DireccionSerializer(many=True, required=True)  # Para direcciones del courier
    
    #IMPORTANTE DESPLEGAR Y LEER
    """
        como no se puede mapear una relacion entre clientecourier , direcciones y clienteDestino
        a la hora de mostrar los campos una vez se hayan guardado,  implement serializers.SerializerMethodField()
        lo que me permite utilizar  direcciones_destino para mostrar o serializer la informacion en el mismo serializer
        ClientCourierCreateSerializer , cuando hago un get , "que es lo que se produce una vez se termina de guarda" , se llama
        al metodo get_direcciones_destino()


        nota: POR QUE NO PASA LO MISMO CON EL CAMPO direcciones ?: SE DEBE A QUE SI HAY UNA RELACION MAPEADA EN EL MODELO DIRECCIONES
            cliente_courier = models.ForeignKey(
                ClientCourier,
                on_delete=models.CASCADE,
                related_name="direcciones",
                null=True,
                blank=True
            )

         QUE RELACIONA DIRECTAMENTE CLIENT CURRIER CON DIRECCIONES A TRAVEZ DE  related_name , EL ERROR PASA CUANDO INTERBIENE clientDestino

         
        nota 2 : tambien pude haber hecho estoo : direcciones_destino = DireccionSerializer(many=True, write_only=True)
        write_only=True es la clave.

    """
    direcciones_destino = serializers.SerializerMethodField()
    
    class Meta:
        model= ClientCourier
        fields = "__all__"


    def get_direcciones_destino(self , obj):
        return DireccionSerializer(obj.usuario_destino.direcciones_destino.all(), many=True).data

        
    @transaction.atomic
    def create (self , validated_data):
        usuario_destino_data = validated_data.pop('usuario_destino')
        direcciones_courier_data = validated_data.pop('direcciones_cliente_courier' , [])
        #IMPORTANTE DESPLEGAR Y LEER
        """
        self.context['request'].data.get('direcciones_destino', []) es la informacion que viene del request , 
        y le paso el request cuando uso el serializador  ClientCourierCreateSerializer en el ClientView para guardar
        
        y no utilizo validated_data poruqe no es un campo declarado explicitamente asi que no pasa a la etapa que monta los datos 
        en validated_data.

        """
        direcciones_destino_data = self.context['request'].data.get('direcciones_destino', [])

        try:
            usuario_destino = ClienteUsuarioDestino.objects.create(**usuario_destino_data)
    
            cliente_courier = ClientCourier.objects.create(
                usuario_destino=usuario_destino,
                **validated_data
            )

            # direcciones courier
            if not direcciones_courier_data:
                raise ValidationError("Debe proporcionar al menos una dirección para el cliente courrier.")
            for direccion_data in direcciones_courier_data:
                Direccion.objects.create(
                    cliente_courier=cliente_courier,
                    **direccion_data
                )

            # direcciones destino
            if not direcciones_destino_data:
                raise ValidationError("Debe proporcionar al menos una dirección para el cliente destino.")
            
            for direccion_data in direcciones_destino_data:
                Direccion.objects.create(
                    cliente_destino=usuario_destino,  # Relación con ClienteUsuarioDestino
                    **direccion_data
                )

            return cliente_courier
        

        except IntegrityError as e:
            raise serializers.ValidationError({
                "error": f"Error de integridad: {str(e)}"
            })
        except ValidationError as e:
            raise serializers.ValidationError({
                "error": f"Error de validacion: {str(e)}"
            })
        
    
#serializer update client courier 
class ClientCourierUpdateSerializer(serializers.ModelSerializer):
    direcciones_cliente_courier = DireccionSerializerEditar(many=True , required=False)

    class Meta:
        model=ClientCourier
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
                    'direcciones_cliente_courier'  # Solo direcciones del courier , solo eso aparte del modelo original tiene permitido recibir
                ]
    @transaction.atomic
    def update(self , instance , validate_data):
        direcciones_data = validate_data.pop("direcciones_cliente_courier" , None)
        cliente = super().update(instance , validate_data)
        if not direcciones_data:
            raise ValidationError("La informacion enviada no contiene direccion de cliente courier")

        # Actualizar direcciones (si se proporcionan)
        if direcciones_data is not None:
            self._update_direcciones(instance, direcciones_data)

        return cliente
    
    def _update_direcciones(self, instance, direcciones_data):

        for dir_data in direcciones_data:
                    if 'id' in dir_data:  # Ahora el ID estará presente
                        Direccion.objects.filter(
                            id=dir_data['id'],
                            cliente_courier=instance
                        ).update(
                            estado=dir_data.get('estado'),
                            municipio=dir_data.get('municipio'),
                            sector=dir_data.get('sector'),
                            casa=dir_data.get('casa'),
                            is_active=dir_data.get('is_active', True)
                        )
            