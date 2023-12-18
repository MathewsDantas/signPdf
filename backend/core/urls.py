from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView
from signPdf.api.views import MyTokenObtainPairView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from signPdf.api.router import router 

schema_view = get_schema_view(
   openapi.Info(
      title="Sign PDF API",
      default_version='v1',
      description="API para assinar documentos PDF",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/login/", MyTokenObtainPairView.as_view(),), 
    path("api/login/refresh", TokenRefreshView.as_view()),

]

urlpatterns += [
   path('api/swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
