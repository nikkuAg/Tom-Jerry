from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSets, SentViewSets, ConfirmViewSets, AuditViewSets, capchaViewset, eKYC, otpGeneratorViewset

router = DefaultRouter()
router.register(r'users', UserViewSets, basename="userdata")
router.register(r'sent', SentViewSets)
router.register(r'confirm', ConfirmViewSets)
router.register(r'audit', AuditViewSets)

urlpatterns = [
    path('', include(router.urls)),
    path('capcha', capchaViewset),
    path('otp', otpGeneratorViewset),
    path('kyc', eKYC)
]
