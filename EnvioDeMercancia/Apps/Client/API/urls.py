from django.urls import path

#from EnvioDeMercancia.Apps.Client.API.views.clientViews import (GeneraListClients, GeneraListClients2  , GeneraListClientSEditarEliminarGet2, GetNaturalOrCourierClient  , ClienteRelacionadoView)

from EnvioDeMercancia.Apps.Client.API.views.AuditoriaClientViews import (AuditClietsView)



from EnvioDeMercancia.Apps.Client.API.views.clientViews import ( GeneraListClients2  , GeneraListClientSEditarEliminarGet2)




urlpatterns = [
    #lista todos y crea
    # path("AllClients/" , GeneraListClients.as_view() , name ="AllClientsName"),
    
    # #edita , elimina y lista uno solo . para los clientes bases
    # path("NaturalOrCourierRetrieve/<int:pk>/" , GetNaturalOrCourierClient.as_view() , name ="NaturalOrCourierRetriveName"),
    
    # #lista y edita clientes relacionados con clientes bases
    # path('clientes-relacionado/<int:pk>/', ClienteRelacionadoView.as_view(), name='cliente-relacionadoName'),

    
    
    #auditoria de clientes
    path("AuditClients/" , AuditClietsView , name="auditClientsName"),

    
    path("AllClients2/" , GeneraListClients2.as_view() , name ="AllClientsName"),

    path("AllClients22/<int:pk>/" , GeneraListClientSEditarEliminarGet2.as_view() , name ="AllClientsName"),


    
    

    
]
