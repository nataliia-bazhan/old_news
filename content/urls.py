from django.urls import path
from . import views

app_name = "content"

urlpatterns = [
    path("comments/", views.all_comments, name="all_comments"),
    path("user_content/", views.user_content, name="user_content"),
    path("submit/", views.create_post, name="submit"),
    path("posts/", views.all_posts, name="posts"),
    path("post/<int:pk>", views.post_details, name="post_details"),
    path("post/<int:pk>/update", views.post_update, name="post_update"),
    path("post/<int:pk>/delete", views.post_delete, name="post_delete"),
    path("comment/<int:pk>/update",
         views.comment_update, name="comment_update"),
    path("comment/<int:pk>/delete",
         views.comment_delete, name="comment_delete"),
    path("posts/vote/<int:pk>", views.post_vote, name="post_vote"),
    path("comments/vote/<int:pk>",
         views.comment_vote, name="comment_vote"),
]
