from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSets, SentViewSets, ConfirmViewSets, AuditViewSets, ClientSentViewSet, capchaViewset, eKYC, otpGeneratorViewset
from .views import PasswordView, UserViewSets, SentViewSets, ConfirmViewSets, AuditViewSets, capchaViewset, eKYC, geoLocation, otpGeneratorViewset, createUser, sentRequest

router = DefaultRouter()
router.register(r'users', UserViewSets, basename="userdata")
router.register(r'sent', SentViewSets)
router.register(r'confirm', ConfirmViewSets)
router.register(r'audit', AuditViewSets)
router.register(r'user_request', ClientSentViewSet)
router.register(r'validate/password', PasswordView, basename="password")

urlpatterns = [
    path('', include(router.urls)),
    path('capcha/', capchaViewset),
    path('otp/<str:capcha>/<str:id>/<str:uid>', otpGeneratorViewset),
    path('kyc/<str:otp>/<str:id>/<str:uid>', eKYC),
    path('geolocaion/<str:loc>/<str:po>/<str:pin>/<str:city>/<str:lat>/<str:lng>', geoLocation),
    path('create/<str:uid>', createUser),
    path('sent/<str:clientId>/<str:introducerId>', sentRequest)

]
