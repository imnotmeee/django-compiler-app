from django.urls import path
from .views import home_page, login_page, logout_page, register_page, profile_page, other_profile_page
from .views_language import create_post, all_post, all_post_with_id, view_post, update_post, delete_post

urlpatterns = [
    path('', home_page, name='home_page'),

    path('login/', login_page, name="login_page"),
    path('logout/', logout_page, name="logout_page"),
    path('register/', register_page, name="register_page"),
    path('profile/', profile_page, name="profile_page"),
    path('profile/<int:id>', other_profile_page, name="other_profile_page"),

    path('posts/', all_post, name="posts-page"),
    path('create-post/', create_post, name="create-post-page"),
    path('update-post/<int:id>', update_post, name="update-post-page"),
    path('post/<int:id>', view_post, name="post"),
    path('delete-post/<int:id>', delete_post, name="delete-post-page"),

    path('run-post/<int:id>', all_post_with_id, name="posts-page-id"),
]
