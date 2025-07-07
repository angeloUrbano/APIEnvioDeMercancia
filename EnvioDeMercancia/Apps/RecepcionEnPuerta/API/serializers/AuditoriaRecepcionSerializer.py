from rest_framework import serializers
from EnvioDeMercancia.Apps.RecepcionEnPuerta.models import CajasAlmacenadas



class CajasAlmacenadasHistoricalSerializer(serializers.ModelSerializer):

    history_user = serializers.SerializerMethodField()
    history_type_display = serializers.SerializerMethodField()
    

    class Meta:
        model = CajasAlmacenadas.historical.model
        fields = [
            'history_id',
            'id',
            'numeroTracking',
            'fecha_hora',
            'wareHouseCreated',
            'is_active',
            'history_date',
            'history_change_reason',
            'history_type',
            'history_type_display',
            'history_user'
        ]

    def get_history_user(self, obj):
      
        if obj.history_user is not None:
            return{
                "usuario":obj.history_user.username,
                "nombre": obj.history_user.name,
                "apellido":obj.history_user.last_name,
                "email":obj.history_user.email
            }   
        return None
    

    def get_history_type_display(self , obj):

        return{
            '+': 'Creación',
            '~': 'Actualización',
            '-': 'Eliminación'
        }.get(obj.history_type, obj.history_type)