from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_dashboard, name='dashboard'),

    path('password/', views.change_password, name='change_password'),
    path('account/', views.update_account_basics, name='update_account_basics'),
    path('profile/', views.update_profile, name='update_profile'),

    path('researcher/', views.researcher_dashboard, name='researcher_dashboard'),
    path('researcher/export_people/', views.export_people, name='export_people'),
    path('researcher/export_moods/', views.export_moods, name='export_moods'),
    path('researcher/export_userlog/', views.export_userlog, name='export_userlog'),

    path('linkworkers/', views.linkworker_list, name='linkworker_list'),
    path('linkworker/', views.linkworker_details, name='linkworker_mydetails'),
    path('linkworker/<int:pk>/details/', views.linkworker_details, name='linkworker_details'),
    # path('linkworker/<int:pk>/export/', views.linkworker_export, name='linkworker_export'),

    path('pacs/', views.pac_list, name='pac_list'),
    path('pac/', views.pac_details, name='pac_mydetails'),
    path('pac/<int:pk>/details/', views.pac_details, name='pac_details'),
    path('pac/<int:pk>/timeline/', views.pac_timeline, name='pac_timeline'),
    path('pac/<int:pk>/export/', views.pac_export, name='pac_export'),
    path('pac/<int:pk>/export/circles/', views.pac_export_circles, name='pac_export_circles'),
    path('pac/<int:pk>/export/userlog/', views.pac_export_userlog, name='pac_export_userlog'),
    path('pac/<int:pk>/moodspider_chart/', views.moodspider_chart, name='moodspider-chart'),
    path('pac/<int:pk>/moodtimeline_chart/', views.moodtimeline_chart, name='moodtimeline-chart'),
    path('pac/<int:pk>/moodsparkline_chart/', views.moodsparkline_chart, name='moodsparkline_chart'),
    # path('membership_chart/', views.membership_chart, name='membership-chart'),
    # path('export/', views.export),
]

