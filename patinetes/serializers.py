from rest_framework import serializers
from patinetes.models import Patinete, Alquiler, Usuario


class PatineteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Patinete
        fields = ['url','numero','tipo','precio_desbloqueo','precio_minuto']


class AlquilerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Alquiler
        fields = ['url', 'usuario','patinete','fecha_desbloqueo','fecha_entrega','coste_final']


class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario
        fields = ['url','debito']