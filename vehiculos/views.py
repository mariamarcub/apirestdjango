from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from vehiculos.models import Marca, Vehiculo
from vehiculos.serializers import GroupSerializer, UserSerializer, MarcaSerializer, VehiculoSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter


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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @extend_schema( #Para filtar el query por la url
        parameters=[
            OpenApiParameter(name='marca', description="", required=False, type=str)
        ]
    )
    @action(detail=False, methods=['get'], description="filter on marca get parameter")
    def filtro_marca(self, request):
        vehiculos_marca = Vehiculo.objects.all()
        marca = self.request.query_params.get('marca')

        if (marca):
            vehiculos_marca = Vehiculo.objects.all().filter(marca__nombre=marca)

        serializer = self.get_serializer(vehiculos_marca, many=True)
        return Response(serializer.data)