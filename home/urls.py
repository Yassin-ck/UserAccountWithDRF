from django.urls import path,include
from . import views
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# from rest_framework_simplejwt.views import TokenObtainPairView

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('',views.UserRegistrationView.as_view(),name='registration'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('profile/',views.UserProfileView.as_view(),name='profile'),
    path('profilecrud/',views.UserProfileEdit.as_view(),name='profilecrud'),
    path('profilecrud/<int:pk>/',views.UserProfileEdit.as_view(),name='profilecrud'),
    
]