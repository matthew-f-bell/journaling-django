from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('journal-entry/', views.Journal_Entry_View.as_view(), name='journal-entry'),
    path('journal-update/<int:pk>', views.Journal_Update_View.as_view(), name='journal-update'),
    path('journal-delete/<int:pk>', views.Journal_Delete_View.as_view(), name='journal-delete'),
    path('user-profile/<int:user_id>', views.profile_view, name='user-profile'),
]