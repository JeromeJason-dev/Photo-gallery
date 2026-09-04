from django.urls import path
from . import views

app_name = "photo_gallery"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("gallery/", views.HomeView.as_view(), name="gallery"), 
    path("photo/<int:pk>/", views.PhotoDetailView.as_view(), name="photo_detail"),
    path("photo/upload/", views.PhotoUploadView.as_view(), name="photo_upload"),
    path("photo/<int:pk>/delete/", views.PhotoDeleteView.as_view(), name="photo_delete"),
    path("photo/<int:pk>/react/<str:value>/", views.react_to_photo, name="react_to_photo"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.PhotoGalleryLoginView.as_view(), name="login"),
    path("logout/", views.PhotoGalleryLogoutView.as_view(), name="logout"),
    path("password-change/", views.PhotoGalleryPasswordChangeView.as_view(), name="password_change"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
]