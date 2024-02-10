from django.contrib.auth.decorators import login_required
from django.db.models import Q
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from patinetes.models import Patinete, Alquiler, Usuario
from patinetes.serializers import PatineteSerializer, AlquilerSerializer, UsuarioSerializer


class PatineteView(viewsets.ModelViewSet):
    queryset = Patinete.objects.all()
    serializer_class = PatineteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] #Con este permiso es suficiente para la autentificación en las funciones internas

    @action(detail=True, methods=['get'])  # El action sirve para crear una acción personalizada
    #detail=True: Indica que la acción personalizada se aplica a un
    #recurso específico dentro de una colección de recursos.
    #Es un patinete en concreto, por eso es detail=True
    def alquilar_patinete(self, request, pk=None): #AQUI EL PATINETE ESTÁ LIBRE
        patinete = Patinete.objects.get(pk=pk)
        patinete_libre = Patinete.objects.filter(Q(alquiler_is_null=True) & Q(alquiler__fecha_entrega_isnull= True))

        if patinete_libre:
            return Response({'mensaje': 'El patinete está disponible para alquilarse'}, status=status.HTTP_200_OK) #Operación exitosa. #Este código de estado indica que la solicitud se ha completado correctamente.
        else: # El patinete ya está alquilado
            return Response({'error': 'El patinete ya está alquilado'}, status=status.HTTP_400_BAD_REQUEST) #Error. Este código de estado indica que la solicitud no pudo ser procesada debido a un error en la solicitud del cliente

    @action(detail=True, methods=['get'])
    def liberar_patinete(self, request, pk=None):

        patinete = Patinete.objects.get(pk=pk)
        alquiler = Alquiler.objects.get(pk=pk)

        # Verificar si el patinete está en alquiler para el usuario actual
        patinete_a_liberar = Alquiler.objects.filter(
            Q(patinete=patinete) &
            Q(usuario=request.user) &
            Q(fecha_entrega__isnull=True) #Tiene fecha de entrega, por lo que va a liberarlo
        ).first()

        tiempo_alquiler = (alquiler.fecha_entrega() - alquiler.fecha_desbloqueo).total_seconds() / 60  # Tiempo en minutos
        coste_final = tiempo_alquiler * patinete.precio_minuto

        usuario = Usuario.objects.get(user=request.user)
        usuario.debito += coste_final
        usuario.save()

        alquiler.fecha_entrega = True
        alquiler.save()

        return Response({'mensaje': 'Patinete liberado exitosamente'}, status=status.HTTP_200_OK)


class AlquilerView(viewsets.ModelViewSet):
    queryset = Alquiler.objects.all()
    serializer_class = AlquilerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UsuarioView(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

