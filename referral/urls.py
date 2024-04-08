from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
   path('register/',views.register_user, name='register'),
   path('detail/',views.UserList, name='detail'),
   path('user/<int:pk>',views.user_detail, name='user-detail'),
   path('login/token',obtain_auth_token, name='create-token'),
]
