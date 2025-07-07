from django.urls import path

from EnvioDeMercancia.Apps.RecepcionEnPuerta.API.views.AuditoriaRecepcionCajaView import AuditoriaRecepcionEnPuerta

urlpatterns =[
    path( "AuditoriaRecepcionEnPuerta/", AuditoriaRecepcionEnPuerta.as_view() ,name ="")

]