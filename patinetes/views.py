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
        patiente_libre = Patinete.objects.filter(Q(alquiler_is_null=True) & Q(alquiler__fecha_entrega_isnull= True))

        if patiente_libre:
            return Response({'mensaje': 'El patinete está disponible para alquilarse'}, status=status.HTTP_200_OK) #Operación exitosa. #Este código de estado indica que la solicitud se ha completado correctamente.
        else: # El patinete ya está alquilado
            return Response({'error': 'El patinete ya está alquilado'}, status=status.HTTP_400_BAD_REQUEST) #Error. Este código de estado indica que la solicitud no pudo ser procesada debido a un error en la solicitud del cliente


    def liberar_patinete(self, request, pk=None):
        alquiler = Alquiler.objects.get(usuario=request.user, patinete_id=pk, finalizado=False)
        costo_alquiler = alquiler.calcular_costo_alquiler()  # Suponiendo que tienes un método en el modelo Alquiler para calcular el costo
        usuario = Usuario.objects.get(user=request.user)
        usuario.debito += costo_alquiler
        usuario.save()
        alquiler.finalizado = True
        alquiler.save()
        patinete = Patinete.objects.get(pk=pk)
        patinete.disponible = True
        patinete.save()
        return Response({'mensaje': 'Patinete liberado exitosamente'}, status=status.HTTP_200_OK)


class AlquilerView(viewsets.ModelViewSet):
    queryset = Alquiler.objects.all()
    serializer_class = AlquilerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UsuarioView(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

