"""Wire URL to view to access the API"""
from django.urls import path   # define different parts in app

from user import views


app_name = 'user'

urlpatterns = [   # routing for user functionality
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
