from rest_framework import routers
from .views import ClientViewSet, DocumentViewSet

router = routers.SimpleRouter()
router.register(r'cliente', ClientViewSet, basename='cliente')
router.register(r'documento', DocumentViewSet, basename='documento')