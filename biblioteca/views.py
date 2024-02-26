from django.db.models import Q
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from biblioteca.models import Libro, Alquiler, Usuario
from biblioteca.serializers import LibroSerializer, AlquilerSerializer, UsuarioSerializer


class LibroView(viewsets.ModelViewSet):
    queryset = Libro.objects.all().order_by('titulo')  # Para que la paginación sea consistente, es frecuente usar el order_by()
    serializer_class = LibroSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Con este permiso es suficiente para la autentificación en las funciones internas

    @action(detail=False, methods=['get'])
    def editoriales(self, request):
        # Obtener el nombre de la editorial proporcionado en la solicitud
        editorial_nombre = request.query_params.get('editorial')

        # Filtrar los libros por el nombre de la editorial si se proporciona
        libros = Libro.objects.all()  # Obtener todos los libros por defecto
        if editorial_nombre:
            libros = libros.filter(editorial=editorial_nombre)

        serializer = AlquilerSerializer(editorial_nombre, many=True, context={'request': request})
        return Response(serializer.data)

class AlquilerView(viewsets.ModelViewSet):
    queryset = Alquiler.objects.all()
    serializer_class = AlquilerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    #Saber que libros son alquilados por mujeres y por hombres
    @action(detail=False, methods=['get'])
    def alquileres_mujer(self, request):
        mujer = Alquiler.objects.filter(Q(usuario__genero='Femenino'))
        serializer = AlquilerSerializer(mujer, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def alquileres_hombre(self, request):
        hombre = Alquiler.objects.filter(Q(usuario__genero='Masculino'))
        serializer = AlquilerSerializer(hombre, many=True, context={'request': request})
        return Response(serializer.data)


class UsuarioView(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]





from django.shortcuts import render

# Create your views here.
