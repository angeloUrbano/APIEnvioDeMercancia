
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



