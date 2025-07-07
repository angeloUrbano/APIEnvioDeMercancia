from rest_framework.routers import DefaultRouter


from EnvioDeMercancia.Apps.RecepcionEnPuerta.API.views.RecepcionCajaView import RecepcionEnPuertaCRUD



router = DefaultRouter()

router.register(r'RecepcionEnPuerta' , RecepcionEnPuertaCRUD , basename="RecepcionEnPuerta")

urlpatterns = router.urls