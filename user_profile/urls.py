from django.urls import path
from . import views


urlpatterns = [
    # path("edit/{edit_field}/", views.create_post, name="create_post"), // UPDATE
    path("edit/username/", views.EditUsername.as_view(), name="Edit Username"),
    path("edit/name/", views.EditName.as_view(), name="Edit Name"),
    path("edit/email/", views.EditEmail.as_view(), name="Edit Email"),
    path("edit/profile-pic/", views.EditProfilepic.as_view(), name="Edit Profile Picture"),
    path("edit/status/", views.EditStatus.as_view(), name="Edit Status"), #Status Text
    path("edit/status-indicator/", views.EditStatusIndicator.as_view(), name="Edit Status Indicator"),
    path("edit/bio/", views.EditBio.as_view(), name="Edit Biography"),
    path("edit/reset-password/", views.ResetPassword.as_view(), name="Reset Password")





    


]