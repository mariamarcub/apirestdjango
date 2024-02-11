from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework import routers
from patinetes import views
from patinetes.views import PatineteView

router = routers.DefaultRouter()

# Definir un enrutador para las vistas basadas en viewsets
router.register(r'patinetes', views.PatineteView)
router.register(r'alquileres', views.AlquilerView)
router.register(r'usuarios', views.UsuarioView)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    #URLS PARA ACCEDER A CADA FUNCIÓN
    path('patinetes/<int:pk>/alquilar/', PatineteView.as_view({'get': 'alquilar_patinete'}), name='alquilar-patinete'),
    path('patinetes/<int:pk>/liberar/', PatineteView.as_view({'get': 'liberar_patinete'}), name='liberar-patinete'),
    path('patinetes/libres/', PatineteView.as_view({'get': 'patinetes_libres'}), name='patinetes-libres'),
    path('patinetes/ocupados/', PatineteView.as_view({'get': 'patinetes_ocupados'}), name='patinetes-ocupados'),
    path('alquileres/alquileresrealizados/', PatineteView.as_view({'get': 'alquileres_realizados'}), name='alquileres-realizados'),
    path('alquileres/listadoalquileres/', PatineteView.as_view({'get': 'listado_alquileres'}), name='listado-alquileres'),

]

urlpatterns += router.urls