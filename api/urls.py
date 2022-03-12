from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("create/post/", views.create_post, name="create_post"),
    path("create/comment/", views.CreateComment.as_view(), name="CreateComment"), # Adds a new comment



    # path("login/", views.dummy_login, name="dummy_login"),
    path("load_posts/", views.load_posts, name="load_posts"),
    path("load_account_posts/", views.load_account_posts, name="load_account_posts"),

    path("load_search_query_posts/", views.get_post_by_search_text, name="load Search query Posts"),

    path("handle_action/post/", views.HandleActionPost.as_view(), name="HandleActionPost"),

    path("handle_action/comment/", views.HandleActionComment.as_view(), name="HandleActionComment"),
]