from django.contrib import admin


# from EnvioDeMercancia.Apps.Client.models import (
#     ClienteUsuarioDestino, 
#     ClienteQuienEnvia,
#     ClienteQuienRecibe, 
#     ClientNatural,
#     ClientCourier,
#     Direccion
# )




from EnvioDeMercancia.Apps.Client.models import (
    ClientNatural,
    Direccion


)



# Register your models here.

# admin.site.register(ClienteUsuarioDestino)
# admin.site.register(ClienteQuienEnvia)
# admin.site.register(ClienteQuienRecibe)
# admin.site.register(ClientNatural)
# admin.site.register(ClientCourier)
# admin.site.register(Direccion)



admin.site.register(ClientNatural)
admin.site.register(Direccion)




