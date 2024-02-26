from rest_framework import serializers
from biblioteca.models import Libro, Alquiler, Usuario


class LibroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Libro
        fields = ['url','usuario','titulo','autor','editorial','anyo_publicacion']


class AlquilerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Alquiler
        fields = ['url', 'libro','usuario','inicio','fin']


class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario
        fields = ['url','user','genero','email']