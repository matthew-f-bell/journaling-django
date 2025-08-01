from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('user-profile/<int:user_id>', views.profile_view, name='user-profile'),
#    path('logout/', views.logout_view, name='logout'),
]