
from network.views import profile_page
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following_page, name="following"),
    path("profile/<str:username>", views.profile_page, name="profile"),
    path("edit/<int:postId>", views.edit, name="edit"),
    path("likes/<int:postID>", views.like, name="like"),
    path("<str:pageName>/<int:pageNum>", views.pages, name="pages"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
