from django.urls import path
from accounts import views 


urlpatterns = [
    path('auth/login/', views.LoginAPIView.as_view(), name="api_login"),
    path('auth/register/', views.RegisterAPIView.as_view(), name="api_register"), 
    path('profile/<int:profile_id>/', views.ProfileByIdAPIView.as_view(), name="api_profile_detail"),   
]