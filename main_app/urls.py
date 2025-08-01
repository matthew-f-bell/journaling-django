from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('journal-entry/', views.Journal_Entry_View.as_view(), name='journal-entry'),
    path('user-profile/<int:user_id>', views.profile_view, name='user-profile'),
]