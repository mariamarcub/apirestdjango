from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from patinetes.models import Patinete, Alquiler, Usuario
from patinetes.serializers import PatineteSerializer, AlquilerSerializer, UsuarioSerializer


class PatineteView(viewsets.ModelViewSet):
    queryset = Patinete.objects.all().order_by('tipo') #Para que la paginación sea consistente, es frecuente usar el order_by()
    serializer_class = PatineteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] #Con este permiso es suficiente para la autentificación en las funciones internas

    #Alquilar: Requiere que el usuario esté autenticado y que indique un Patinete libre.
    @action(detail=True, methods=['get'])  # El action sirve para crear una acción personalizada
    #detail=True: Indica que la acción personalizada se aplica a un
    #recurso específico dentro de una colección de recursos.
    #Es un patinete en concreto, por eso es detail=True
    def alquilar_patinete(self, request, pk=None): #AQUI EL PATINETE ESTÁ LIBRE
        patinete = Patinete.objects.get(pk=pk)
        #alquiler_is_null = true significa que no existe ningún alquiler
        #alquiler__fecha_entrega_isnull = False significa que está libre el patinete
        patinete_libre = Patinete.objects.filter(Q(alquiler_is_null=True) & Q(alquiler__fecha_entrega_isnull= False))

        if patinete_libre:
            return Response({'mensaje': 'El patinete está disponible para alquilarse'}, status=status.HTTP_200_OK) #Operación exitosa. #Este código de estado indica que la solicitud se ha completado correctamente.
        else: # El patinete ya está alquilado
            return Response({'error': 'El patinete ya está alquilado'}, status=status.HTTP_400_BAD_REQUEST) #Error. Este código de estado indica que la solicitud no pudo ser procesada debido a un error en la solicitud del cliente

    #Si se está enviando un mensaje, no se necesita el serializer.

    #Liberar: Requiere que el usuario esté autenticado y que indique
    # el patinete que tiene en alquiler y quiere liberar.
    # La liberación implica calcular el coste final y aumentar el débito del usuario.
    @transaction.atomic
    @action(detail=True, methods=['get'])
    def liberar_patinete(self, request, pk=None):

        patinete = Patinete.objects.get(pk=pk)
        alquiler = Alquiler.objects.get(pk=pk)

        # Verificar si el patinete está en alquiler para el usuario actual
        patinete_a_liberar = Alquiler.objects.filter(
            Q(patinete=patinete) &
            Q(usuario=request.user) &
            Q(fecha_entrega__isnull=True) #Sigue ocupado porque la intención es liberarlo, entonces todavía, no tiene fecha de entrega
        ).first()

        tiempo_alquiler = (alquiler.fecha_entrega - alquiler.fecha_desbloqueo).total_seconds() / 60  # Tiempo en minutos
        coste_final = tiempo_alquiler * patinete.precio_minuto

        usuario = Usuario.objects.get(user=request.user)
        usuario.debito += coste_final
        usuario.save()

        alquiler.fecha_entrega = datetime.now()
        alquiler.save()

        return Response({'mensaje': 'Patinete liberado exitosamente'}, status=status.HTTP_200_OK)

        #AMPLIACIÓN

        #Crea un servicio que muestre los patinetes libres.
        @action(detail=False, methods=['get'])
        def patinetes_libres(self, request):
            #alquiler_isnull = False significa que el patinete está alquilado, no está libre
            #fecha_entrega__isnull=True significa el patinete está actualmente alquilado y aún no ha sido devuelto.
            #Exclude sirve para decirnos que nos QUITE los que están alquilados y los no entregados.
            libres = Patinete.objects.exclude(Q(alquiler__isnull=False) & Q(alquiler__fecha_entrega__isnull=True))
            # Serializar los datos de los patinetes libres si es necesario
            serializer = PatineteSerializer(libres, many=True)

            # Devolver los datos de los patinetes libres como respuesta
            return Response(serializer.data)
        #Crea un servicio que muestre los patinetes ocupados.
        @action(detail=False, methods=['get'])
        def patinetes_libres(self, request):
            #alquiler_isnull = False significa que el patinete está alquilado, no está libre
            #fecha_entrega__isnull=True significa el patinete está actualmente alquilado y aún no ha sido devuelto.
            #Con filter le decimos que nos muestre aquellos que cumplan esas condiciones: alquilado y no entregado
            ocupados = Patinete.objects.filter(Q(alquiler__isnull=False)&Q(alquiler__fecha_entrega__isnull=True))
            # Serializar los datos de los patinetes ocupados si es necesario
            serializer = PatineteSerializer(ocupados, many=True)
            # Devolver los datos de los patinetes ocupados como respuesta
            return Response(serializer.data)

class AlquilerView(viewsets.ModelViewSet):
    queryset = Alquiler.objects.all()
    serializer_class = AlquilerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #Publica un servicio para el listado de todos los alquileres
    # realizados que sólo puedan ver los administradores.

    #Publica un servicio para el listado de todos los alquileres realizados
    # que sólo puedan ver los administradores
    @transaction.atomic
    @action(detail=False, methods=['get'])
    @permission_classes([IsAdminUser]) #Solo puede verlo los administradores
    def alquileres_realizados(self, request):
        # Obtener todos los alquileres sin entregar
        alquileres_activos = Alquiler.objects.filter(patinete__alquilerset__fecha_entrega=None)
        serializer = AlquilerSerializer(alquileres_activos, many=True)
        return Response(serializer.data)


    #Publica un servicio para el listado de los alquileres que solo pueda
    # ver el usuario autenticado sobre sí mismo.

    @action(detail=False, methods=['get'])
    def listado_alquileres(self, request):
        usuario_autenticado = request.user
        alquileres_activos = Alquiler.objects.filter(Q(fecha_entrega__isnull=False))
        # Filtrar los alquileres activos del usuario autenticado
        alquileres_activos_usuario = alquileres_activos.filter(usuario=usuario_autenticado)
        # Serializar y devolver los alquileres activos del usuario autenticado
        serializer = AlquilerSerializer(alquileres_activos_usuario, many=True)
        return Response(serializer.data)

class UsuarioView(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

