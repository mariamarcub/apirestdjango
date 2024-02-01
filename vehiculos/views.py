from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from vehiculos.models import Marca, Vehiculo
from vehiculos.serializers import GroupSerializer, UserSerializer, MarcaSerializer, VehiculoSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class MarcaView(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer

    @action(detail=True, methods=['get'])  # El action sirve para crear una acción personalizada que liste los vehículos de una marca específica
    def listarVehiculosPorMarca(self, request, pk):
        marca = get_object_or_404(Marca, pk=pk)  # obtener la marca correspondiente basada en el pk proporcionado en la URL
        vehiculos = Vehiculo.objects.filter(marca=marca)  # Obtener todos los vehículos asociados a la marca
        serializer = VehiculoSerializer(vehiculos, many=True,context={'request':request})  # Serializar los vehículos
        return Response(serializer.data)  # Devolver la lista de vehículos como respuesta
        # serializer.data: se accede a los datos serializados del objeto serializer


class VehiculoView(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
