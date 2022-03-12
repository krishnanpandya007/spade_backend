from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", login_required(views.HomeStaffView.as_view(), login_url='/abc/login/'), name="home"),
    # path("signup/", views.signup, name="signup"),
    # path("check_mail/", views.check_mail, name="check_mail"),
    # path("verify/<slug:auth_token>", views.verify, name="verify"),
    path("login/", views.login, name="login"),
    # path("load_more_posts/", views.load_more_posts, name="load_more_posts"),
    # path("trial/", views.trial, name="trial"),
    # path("create-post/",views.create_post,name="create_post"),
    # path("handle_action/submit_feedback/", views.submit_feedback, name="submit_feedback"),
    # path('handle_action/like/', views.handle_like, name="handle_like"),
    # path('handle_action/dislike/', views.handle_dislike, name="handle_dislike"),
    # path("load_relevant_posts/", views.load_relevant_posts, name="load_relevant_posts"),
      # path("signup/signupuser", views.signupuser, name="signupuser")
]