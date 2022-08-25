from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.urls import path
import wallet.views
import main.views


router = DefaultRouter()
router.register(r"register", main.views.RegistrationViewSet, basename="main")
router.register(r"wallets", wallet.views.WalletViewSet, basename="wallets")

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += router.urls