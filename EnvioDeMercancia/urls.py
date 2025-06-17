"""EnvioDeMercancia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path , include
from EnvioDeMercancia.Apps.User.API.views.viewsUser import Login , Logout
#from EnvioDeMercancia.Apps.Client.API.urls import ()


from rest_framework_simplejwt.views import (

    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    #admin path
    path('admin/', admin.site.urls),

    #users path
    path('Users/',include("EnvioDeMercancia.Apps.User.API.routers")),
    path('Login/', Login.as_view() , name ="login"),
    path('Logout/', Logout.as_view() , name = "logout" ),

    #Client
    path('Clients/',include("EnvioDeMercancia.Apps.Client.API.urls")),

    #token jwt path
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
