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
    direcciones_cliente_natural = DireccionSerializerEditar(many=True , required=False)


    class Meta:
        model=ClientNatural
        fields=[
                'nombre',
                'apellido',
                'identificacion',
                'correo',
                'correo_aux',
                'telefono',
                'telefono_aux',
                'codigo_cliente',
                'is_active',
                'direcciones_cliente_natural'  # Solo direcciones del courier , solo eso aparte del modelo original tiene permitido recibir
            ]


    def update(self , instance , validated_data):
        direcciones_data = validated_data.pop("direcciones_cliente_natural" , None)
        cliente = super().update(instance , validated_data)

        if direcciones_data is not None:
            self._update_direcciones(instance, direcciones_data)

        return cliente
    
    def _update_direcciones(self, instance, direcciones_data):

        for dir_data in direcciones_data:
                    if 'id' in dir_data:  # Ahora el ID estará presente
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
            
            






#client Destino  ------------------------------------------->>>>>>>>>>>>>>>>>

class ClienteDestinoSerializer(serializers.ModelSerializer):
    direcciones_destino =  DireccionSerializerEditar(many=True)

    class Meta:
        model=ClienteUsuarioDestino
        fields = '__all__'
        extra_kwargs = {
            'identificacion': {'validators': []},  # Desactiva validadores automáticos
            'correo': {'validators': []},
            'correo_aux': {'validators': []}
        }


class ClientCourierDestinoSerializer(serializers.ModelSerializer):
    usuario_destino = ClienteDestinoSerializer(read_only=True)

    class Meta:
        model=ClientCourier
        fields=["nombre" , "apellido" , "usuario_destino"]


class ClientCourierDestinoUpdateSerializer(serializers.ModelSerializer):
    usuario_destino = ClienteDestinoSerializer()
    

    class Meta:
        model=ClientCourier
        fields=["nombre" , "apellido" , "usuario_destino"]  


    def update(self , instance , validated_data):
        usuario_destino_data = validated_data.pop('usuario_destino', {})
        direcciones_data = usuario_destino_data.pop('direcciones_destino', None)


        if usuario_destino_data:
            usuario_destino = instance.usuario_destino
            for attr, value in usuario_destino_data.items():
                setattr(usuario_destino, attr, value)
            
            # Validar manualmente los campos únicos
            self.validate_unique_usuario_destino(usuario_destino)
            usuario_destino.save()


        if direcciones_data is not None:
            self._update_direcciones(usuario_destino, direcciones_data)
                
        return instance

    def _update_direcciones(self, instance, direcciones_data):

        for dir_data in direcciones_data:
                    
                    print(dir_data , "/*/*//*/*/*")
                    
                    if 'id' in dir_data:  # Ahora el ID estará presente
                        Direccion.objects.filter(
                            id=dir_data['id'],
                           cliente_destino=instance
                        ).update(
                            estado=dir_data.get('estado'),
                            municipio=dir_data.get('municipio'),
                            sector=dir_data.get('sector'),
                            casa=dir_data.get('casa'),
                            is_active=dir_data.get('is_active', True)
                        )


    def validate_unique_usuario_destino(self, instance):
        """Valida manualmente los campos únicos"""
        errors = {}
        
        if ClienteUsuarioDestino.objects.exclude(pk=instance.pk).filter(identificacion=instance.identificacion).exists():
            errors['identificacion'] = ["Esta identificación ya está en uso"]
        
        if ClienteUsuarioDestino.objects.exclude(pk=instance.pk).filter(correo=instance.correo).exists():
            errors['correo'] = ["Este correo ya está en uso"]
        
        if instance.correo_aux and ClienteUsuarioDestino.objects.exclude(pk=instance.pk).filter(correo_aux=instance.correo_aux).exists():
            errors['correo_aux'] = ["Este correo auxiliar ya está en uso"]
        
        if errors:
            raise serializers.ValidationError({'usuario_destino': errors})






#client quien envia  ------------------------------------------->>>>>>>>>>>>>>>>>




class ClienteQuienEnviaSerializer(serializers.ModelSerializer):
    direcciones_quien_envia = DireccionSerializerEditar(many=True)

    class Meta:
        model=ClienteQuienEnvia
        fields = "__all__"
        extra_kwargs = {
            'identificacion': {'validators': []},  # Desactiva validadores automáticos
            'correo': {'validators': []},
            'correo_aux': {'validators': []}
        }

        

class ClientNaturalQuienEnviaSerializer(serializers.ModelSerializer):
    quien_envia = ClienteQuienEnviaSerializer(read_only=True)

    class Meta:
        model =ClientNatural
        fields =["nombre" , "apellido" , "quien_envia"]


class ClientNaturalQuienEnviaUpdateSerializer(serializers.ModelSerializer):

    quien_envia = ClienteQuienEnviaSerializer()

    class Meta:
        model =ClientNatural
        fields =["nombre" , "apellido" , "quien_envia"]


    def update(self , instance , validated_data):
        quien_envia_data = validated_data.pop("quien_envia" ,{})
        direcciones_data = quien_envia_data.pop("direcciones_quien_envia" , None)

        if quien_envia_data:
            quien_envia = instance.quien_envia
            for attr, value in quien_envia_data.items():
                setattr(quien_envia, attr, value)
            
            # Validar manualmente los campos únicos
            self.validate_unique_quien_envia(quien_envia)
            quien_envia.save()


        if direcciones_data is not None:
            self._update_direcciones(quien_envia, direcciones_data)
                
        return instance


    def _update_direcciones(self, instance, direcciones_data):

        for dir_data in direcciones_data:
                    
                    print(dir_data , "/*/*//*/*/*")
                    
                    if 'id' in dir_data:  # Ahora el ID estará presente
                        Direccion.objects.filter(
                            id=dir_data['id'],
                           cliente_quien_envia=instance
                        ).update(
                            estado=dir_data.get('estado'),
                            municipio=dir_data.get('municipio'),
                            sector=dir_data.get('sector'),
                            casa=dir_data.get('casa'),
                            is_active=dir_data.get('is_active', True)
                        )


    def validate_unique_quien_envia(self, instance):
        """Valida manualmente los campos únicos"""
        errors = {}
        
        if ClienteQuienEnvia.objects.exclude(pk=instance.pk).filter(identificacion=instance.identificacion).exists():
            errors['identificacion'] = ["Esta identificación ya está en uso"]
        
        if ClienteQuienEnvia.objects.exclude(pk=instance.pk).filter(correo=instance.correo).exists():
            errors['correo'] = ["Este correo ya está en uso"]
        
        if instance.correo_aux and ClienteQuienEnvia.objects.exclude(pk=instance.pk).filter(correo_aux=instance.correo_aux).exists():
            errors['correo_aux'] = ["Este correo auxiliar ya está en uso"]
        
        if errors:
            raise serializers.ValidationError({'usuario_destino': errors})








#client quien recibe  ------------------------------------------->>>>>>>>>>>>>>>>>

class ClienteQuienRecibeSerializer(serializers.ModelSerializer):

    direcciones_quien_recibe = DireccionSerializerEditar(many=True)

    class Meta:
        model = ClienteQuienRecibe
        fields = "__all__"
        extra_kwargs = {
            'identificacion': {'validators': []},  # Desactiva validadores automáticos
            'correo': {'validators': []},
            'correo_aux': {'validators': []}
        }




class ClientNaturalQuienRecibeSerializer(serializers.ModelSerializer):

    quien_recibe = ClienteQuienRecibeSerializer(read_only=True)

    class Meta:
        model = ClientNatural
        fields=["nombre" , "apellido" , "quien_recibe"]





class ClientNaturalQuienRecibeUpdateSerializer(serializers.ModelSerializer):

    quien_recibe = ClienteQuienRecibeSerializer()

    class Meta:
        model= ClientNatural
        fields=["nombre" , "apellido" ,  "quien_recibe"]

    def update(self , instance ,validated_data ): 
        quien_recibe_data = validated_data.pop("quien_recibe" , {})
        direcciones_data   =  quien_recibe_data.pop("direcciones_quien_recibe" , None)


        
        if quien_recibe_data:
            quien_recibe = instance.quien_recibe
            for attr, value in quien_recibe_data.items():
                setattr(quien_recibe, attr, value)
            
            # Validar manualmente los campos únicos
            self.validate_unique_quien_recibe(quien_recibe)
            quien_recibe.save()


        if direcciones_data is not None:
            self._update_direcciones(quien_recibe, direcciones_data)
                
        return instance


    def _update_direcciones(self, instance, direcciones_data):

        for dir_data in direcciones_data:
                    
                    print(dir_data , "/*/*//*/*/*")
                    
                    if 'id' in dir_data:  # Ahora el ID estará presente
                        Direccion.objects.filter(
                            id=dir_data['id'],
                           cliente_quien_recibe=instance
                        ).update(
                            estado=dir_data.get('estado'),
                            municipio=dir_data.get('municipio'),
                            sector=dir_data.get('sector'),
                            casa=dir_data.get('casa'),
                            is_active=dir_data.get('is_active', True)
                        )


    def validate_unique_quien_recibe(self, instance):
        """Valida manualmente los campos únicos"""
        errors = {}
        
        if ClienteQuienEnvia.objects.exclude(pk=instance.pk).filter(identificacion=instance.identificacion).exists():
            errors['identificacion'] = ["Esta identificación ya está en uso"]
        
        if ClienteQuienEnvia.objects.exclude(pk=instance.pk).filter(correo=instance.correo).exists():
            errors['correo'] = ["Este correo ya está en uso"]
        
        if instance.correo_aux and ClienteQuienEnvia.objects.exclude(pk=instance.pk).filter(correo_aux=instance.correo_aux).exists():
            errors['correo_aux'] = ["Este correo auxiliar ya está en uso"]
        
        if errors:
            raise serializers.ValidationError({'usuario_destino': errors})
