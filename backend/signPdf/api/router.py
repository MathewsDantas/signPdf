from rest_framework import routers
from .views import ClientViewSet

router = routers.SimpleRouter()
router.register(r'cliente', ClientViewSet, basename='cliente')