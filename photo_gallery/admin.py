from django.contrib import admin

from .models import Like, Photo, Profile, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("title", "uploaded_by", "created_at", "like_count", "dislike_count")
    list_filter = ("tags", "created_at")
    search_fields = ("title", "description")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "photo", "value", "created_at")
    list_filter = ("value",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "bio")
