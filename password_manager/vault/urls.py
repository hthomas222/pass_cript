# core/urls.py
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from vault import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # Auth views
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="vault/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # Vault views
    path("", views.dashboard, name="dashboard"),
    path("add/", views.add_password, name="add_password"),
    path("edit/<int:entry_id>/", views.edit_password, name="edit_password"),
    path(
        "delete/<int:entry_id>/",
        views.delete_password,
        name="delete_password",
    ),
    path("decrypt/<int:entry_id>/", views.decrypt_api, name="decrypt_api"),
]
