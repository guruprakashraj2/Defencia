from django.urls import path
from . import views 

app_name='App'
urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("login", views.login_view, name="login"),
    path("Register", views.Register, name="Register"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("logout/", views.logout, name="logout"), 
    path("about/",views.about,name="about"),
    path("leadership/",views.leadership,name="leadership"),
    path("vision_mission/",views.vision_mission,name="vision_mission"),
    path("cybersecurity/",views.cybersecurity, name="cybersecurity"),
    path("webappdevelopment/", views.webappdevelopment, name="webappdevelopment"),
    path("penetrationtester/", views.penetrationtester, name="penetrationtester"),
    path("mobiledevelopment/", views.mobiledevelopment, name="mobiledevelopment"),
    path("jobopenings/", views.jobopenings, name="jobopenings"),
    path("internships/", views.internships, name="internships"),
    path("whyjoinus/", views.whyjoinus, name="whyjoinus"),
    path("contact/", views.contact_view, name="contact"),
    path('forget-password/', views.forget_password, name='forget_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
]
