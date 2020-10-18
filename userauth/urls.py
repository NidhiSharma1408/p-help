from django.conf.urls import url
from django.urls import path,include
from rest_framework import routers
from userauth import views
from rest_framework_simplejwt import views as jwt_views
router = routers.DefaultRouter()
router.register(r'', views.UserViewSet)
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('user/',include(router.urls)),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', views.OTPVerificationView.as_view()),
    path('password/reset/', views.PasswordResetView.as_view()),
    path('password/reset/verify/', views.PasswordResetOTPConfirmView.as_view()),
    path('otp/resend/', views.OTPResend.as_view()), 
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

