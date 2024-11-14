from django.urls import path
from .views import UserRegistrationView, UserDetailView

urlpatterns = [
    path('', UserRegistrationView.as_view(), name='user_register'),
    path('<str:username>/', UserDetailView.as_view(), name='user_detail'),
]