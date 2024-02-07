from email.headerregistry import Group

from rest_framework import serializers
from rest_framework.authtoken.admin import User

from vehiculos.models import Marca, Vehiculo

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class MarcaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Marca
        fields = ['url','nombre']


class VehiculoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vehiculo
        fields = ['url', 'marca','tipo_vehiculo','chasis','modelo','matricula','color','fecha_fabricacion','fecha_matriculacion','fecha_baja','suspendido']