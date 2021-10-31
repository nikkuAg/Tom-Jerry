from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSets, SentViewSets, ConfirmViewSets, AuditViewSets, ClientSentViewSet, capchaViewset, eKYC, otpGeneratorViewset

router = DefaultRouter()
router.register(r'users', UserViewSets, basename="userdata")
router.register(r'sent', SentViewSets)
router.register(r'confirm', ConfirmViewSets)
router.register(r'audit', AuditViewSets)
router.register(r'user_request', ClientSentViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('capcha/', capchaViewset),
    path('otp/<str:capcha>/<str:id>/<str:uid>', otpGeneratorViewset),
    path('kyc/<str:otp>/<str:id>/<str:uid>', eKYC)
]
