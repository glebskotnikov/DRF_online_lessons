from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from users.apps import UsersConfig

app_name = UsersConfig.name

router = DefaultRouter()
router.register('', UserViewSet, basename="users")

urlpatterns = [
              ] + router.urls
