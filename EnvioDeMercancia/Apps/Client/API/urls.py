from django.urls import path

from EnvioDeMercancia.Apps.Client.API.views.clientViews import (GeneraListClients , GetNaturalOrCourierClient , ClientCourierDestinoView   , ClientNaturalQuienEnviaView  , ClientNaturalQuienRecibeView )


urlpatterns = [
    #lista todos y crea
    path("AllClients/" , GeneraListClients.as_view() , name ="AllClientsName"),
    
    #edita , elimina y lista uno solo . para los clientes bases
    path("NaturalOrCourierRetrive/<int:pk>/" , GetNaturalOrCourierClient.as_view() , name ="NaturalOrCourierRetriveName"),
    

    #lista y edita clientes relacionados a clientes bases
    path('clientes-courier/<int:pk>/destino/', ClientCourierDestinoView.as_view(), name='cliente-courier-destino'),
    path('clientes-natural/<int:pk>/quienEnvia/', ClientNaturalQuienEnviaView.as_view(), name='cliente-natural-quienEnvia'),
    path('clientes-natural/<int:pk>/quienRecibe/', ClientNaturalQuienRecibeView.as_view(), name='cliente-natural-quienRecibe'),


    
    
]
