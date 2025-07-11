from django.urls import path
from users.views import register, sign_in, sign_out, activate_user

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', sign_in, name='login'),
    path('sign-out/', sign_out, name='logout'),
    path('activate/<int:user_id>/<str:token>/', activate_user),
]
