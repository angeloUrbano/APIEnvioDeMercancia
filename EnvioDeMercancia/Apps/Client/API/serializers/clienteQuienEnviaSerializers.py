
from rest_framework import serializers

#django
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.db import transaction


from EnvioDeMercancia.Apps.Client.models import (
    ClienteQuienEnvia,
    ClientNatural,
    Direccion
)




from EnvioDeMercancia.Apps.Client.API.serializers.direccionesSerializers import DireccionSerializer ,DireccionSerializerEditar




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

    @transaction.atomic
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



