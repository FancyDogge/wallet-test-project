from rest_framework.routers import DefaultRouter
from wallet import views


router = DefaultRouter()
router.register(r"wallets", views.WalletViewSet, basename="wallets")

urlpatterns = router.urls
