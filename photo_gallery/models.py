from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Tag(models.Model):
    """A label used to categorize photos (e.g. 'portrait', 'nature')."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Photo(models.Model):
    """A single photo / portrait / artwork entry in the gallery."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="photos/%Y/%m/")
    tags = models.ManyToManyField(Tag, related_name="photos", blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="photos",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("photo_gallery:photo_detail", kwargs={"pk": self.pk})

    @property
    def like_count(self):
        return self.interactions.filter(value=Like.LIKE).count()

    @property
    def dislike_count(self):
        return self.interactions.filter(value=Like.DISLIKE).count()

    def interaction_for(self, user):
        """Return the current user's interaction (Like instance) with this photo, if any."""
        if not user or not user.is_authenticated:
            return None
        return self.interactions.filter(user=user).first()


class Like(models.Model):
    """Records a user's like or dislike of a photo. One interaction per user/photo."""
    LIKE = 1
    DISLIKE = -1
    VALUE_CHOICES = (
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="photo_interactions"
    )
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name="interactions")
    value = models.SmallIntegerField(choices=VALUE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "photo"], name="unique_user_photo_interaction")
        ]

    def __str__(self):
        return f"{self.user} {'liked' if self.value == self.LIKE else 'disliked'} {self.photo}"


class Profile(models.Model):
    """Extra information attached to each Django User."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"