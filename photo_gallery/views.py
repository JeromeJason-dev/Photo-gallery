from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import (
    PhotoForm,
    ProfileForm,
    RegisterForm,
    StyledAuthenticationForm,
    StyledPasswordChangeForm,
    UserUpdateForm,
)
from .models import Like, Photo, Tag

# Authentication

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "photo_gallery/register.html"
    success_url = reverse_lazy("photo_gallery:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Welcome! Your account has been created.")
        return response


class PhotoGalleryLoginView(LoginView):
    template_name = "photo_gallery/login.html"
    authentication_form = StyledAuthenticationForm


class PhotoGalleryLogoutView(LogoutView):
    next_page = reverse_lazy("photo_gallery:home")


class PhotoGalleryPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "photo_gallery/password_change.html"
    form_class = StyledPasswordChangeForm
    success_url = reverse_lazy("photo_gallery:profile")

    def form_valid(self, form):
        messages.success(self.request, "Your password has been updated.")
        return super().form_valid(form)

# Profile

@login_required
def profile_view(request):
    return render(request, "photo_gallery/profile.html", {"profile_user": request.user})


@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("photo_gallery:profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    return render(
        request,
        "photo_gallery/profile_edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )

# Gallery

class HomeView(ListView):
    model = Photo
    template_name = "photo_gallery/home.html"
    context_object_name = "photos"
    paginate_by = 12

    def get_queryset(self):
        qs = Photo.objects.all().prefetch_related("tags")
        tag_slug = self.request.GET.get("tag")
        query = self.request.GET.get("q")
        if tag_slug:
            qs = qs.filter(tags__slug=tag_slug)
        if query:
            qs = qs.filter(Q(title__icontains=query) | Q(description__icontains=query))
        return qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        context["active_tag"] = self.request.GET.get("tag", "")
        context["query"] = self.request.GET.get("q", "")
        return context


class PhotoDetailView(DetailView):
    model = Photo
    template_name = "photo_gallery/photo_detail.html"
    context_object_name = "photo"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_interaction"] = self.object.interaction_for(self.request.user)
        return context


class PhotoUploadView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = "photo_gallery/photo_form.html"

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Photo uploaded successfully.")
        return response


class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Photo
    template_name = "photo_gallery/photo_confirm_delete.html"
    success_url = reverse_lazy("photo_gallery:home")

    def test_func(self):
        # Allow deletion only if the user uploaded the photo or is staff/superuser
        photo = self.get_object()
        return self.request.user == photo.uploaded_by or self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, "Photo deleted successfully.")
        return super().form_valid(form)

# Likes / Dislikes

@login_required
@require_POST
def react_to_photo(request, pk, value):
    """Toggle a like/dislike interaction for the current user on a photo."""
    photo = get_object_or_404(Photo, pk=pk)
    value = Like.LIKE if value == "like" else Like.DISLIKE

    interaction, created = Like.objects.get_or_create(
        user=request.user, photo=photo, defaults={"value": value}
    )
    if not created:
        if interaction.value == value:
            # Clicking the same reaction again removes it.
            interaction.delete()
            interaction = None
        else:
            interaction.value = value
            interaction.save()

    data = {
        "like_count": photo.like_count,
        "dislike_count": photo.dislike_count,
        "user_reaction": interaction.value if interaction else None,
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse(data)

    return redirect("photo_gallery:photo_detail", pk=photo.pk)