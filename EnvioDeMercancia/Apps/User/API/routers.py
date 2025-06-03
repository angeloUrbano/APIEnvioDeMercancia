from rest_framework.routers import DefaultRouter

from EnvioDeMercancia.Apps.User.API.views.viewsUser import UsersCrudViewSet


router = DefaultRouter()
router.register(r'UsersCrudView' , UsersCrudViewSet  , basename='UsersCrudView')

urlpatterns = router.urls