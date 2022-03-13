"""spade URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

# from rest_framework import routers
# from spado_ubuntu import views

# router = routers.DefaultRouter()
# router.register('', views.HomeView, 'home')

# ex. path="127.0.0.1:8000/home/sleep"-->takes/home and pass "sleep" to included folder!
urlpatterns = [

    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/token/verify/', TokenVerifyView.as_view()),
    path('admin/', admin.site.urls),
    path('apio/', include("api.urls")),
    path('abc/', include("spado_ubuntu.urls")),
    path('account/', include("account.urls")),
    path('profile/', include("user_profile.urls")),

    # path('accounts/', include('allauth.urls')),
    # path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)

