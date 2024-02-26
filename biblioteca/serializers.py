from rest_framework import serializers
from biblioteca.models import Libro, Alquiler, Usuario


class LibroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Libro
        fields = ['url','titulo','autor','editorial','anyo_publicacion']


# En el serializador de Alquiler, asegúrate de serializar correctamente los campos
# relacionales como el libro y el usuario asociados con cada alquiler.
# Validación de fechas: Implementa validación en el serializador para asegurarte
# de que la fecha de inicio del alquiler sea anterior a la fecha de finalización,
# si se proporciona una fecha de finalización.

class AlquilerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Alquiler
        fields = ['url', 'libro','usuario','inicio','fin']
        validators = [
            #asegurarse de que no haya dos alquileres para el mismo libro
            serializers.UniqueTogetherValidator(
                queryset=Alquiler.objects.all(),
                fields=['libro', 'inicio'],
                message="Ya existe un alquiler para este libro en la fecha de inicio"
            ),
            serializers.UniqueTogetherValidator(
                queryset=Alquiler.objects.all(),
                fields=['libro', 'fin'],
                message="Ya existe un alquiler para este libro en la fecha de finalización"
            )
        ]

    def validate(self, data):
        inicio = data.get('inicio')
        fin = data.get('fin')

        if inicio and fin and inicio > fin:
            raise serializers.ValidationError("La fecha de inicio debe ser anterior a la fecha de finalización")
        return data


class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Usuario
        fields = ['url','usuario','genero','email']