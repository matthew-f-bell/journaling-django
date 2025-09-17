from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('journal-entry/', views.Journal_Entry_View.as_view(), name='journal-entry'),
    path('journal-update/<int:pk>', views.Journal_Update_View.as_view(), name='journal-update'),
    path('journal-delete/<int:pk>', views.Journal_Delete_View.as_view(), name='journal-delete'),
    path('user-profile/<int:user_id>', views.Profile_View.as_view(), name='user-profile'),
    path('user-update/<int:pk>', views.Profile_Update_View.as_view(), name='user-update'),
    path('create-daily-goal/', views.Daily_Goals_Create_View.as_view(), name='daily-goals-create'),
    path('check-daily-goals/<int:user_id>', views.Daily_Goals_Checklist_View.as_view(), name='daily-goals-checklist'),
    path('daily-goals-delete/<int:pk>', views.Daily_Goals_Delete_View.as_view(), name='daily-goals-delete'),
    path('daily-goals-update/', views.Daily_Goals_Update_View.as_view(), name='daily-goals-update')
]