from django.urls import path
from account.views import LoadProfileView, RegisterView, GetUserDetailsView, AdminUserInfo
 

urlpatterns = [
    path("register/", RegisterView.as_view(), name="home"),
    path("user/", GetUserDetailsView.as_view()),
    path("load_profile/", LoadProfileView.as_view(), name="Load User Profile"),

    path("is-staff/", AdminUserInfo.as_view(), name="Admin User Authentication")
    
]