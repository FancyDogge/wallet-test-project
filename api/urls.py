from rest_framework.routers import DefaultRouter
from api import views


router = DefaultRouter()
router.register(r"wallets", views.WalletViewSet, basename="wallets")
router.register(r"users", views.RegistrationViewSet, basename="users")

urlpatterns = router.urls
