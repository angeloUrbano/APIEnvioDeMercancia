from rest_framework import serializers


from EnvioDeMercancia.Apps.RecepcionEnPuerta.models import CajasAlmacenadas


class RecepcionEnPuertaCRUDSerializers(serializers.ModelSerializer):
    class Meta:
        model= CajasAlmacenadas
        fields = "__all__"