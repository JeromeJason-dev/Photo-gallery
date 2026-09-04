from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Photo, Profile, Tag


TAILWIND_INPUT = (
    "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm "
    "focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
)


class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": TAILWIND_INPUT})


class StyledPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": TAILWIND_INPUT})


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": TAILWIND_INPUT})
        
        # Override the password help text to only show the character requirement
        if "password1" in self.fields:
            self.fields["password1"].help_text = "Your password must contain at least 8 characters."
        
        # Optional: Remove the default username help text
        if "username" in self.fields:
            self.fields["username"].help_text = ""

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "avatar"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4, "class": TAILWIND_INPUT}),
            "avatar": forms.ClearableFileInput(attrs={"class": "block w-full text-sm text-gray-700"}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": TAILWIND_INPUT})


class PhotoForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Comma-separated tags, e.g. nature, sunset, travel",
        widget=forms.TextInput(attrs={"class": TAILWIND_INPUT, "placeholder": "nature, sunset, travel"}),
    )

    class Meta:
        model = Photo
        fields = ["title", "description", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": TAILWIND_INPUT}),
            "description": forms.Textarea(attrs={"rows": 4, "class": TAILWIND_INPUT}),
            "image": forms.ClearableFileInput(attrs={"class": "block w-full text-sm text-gray-700"}),
        }

    def save(self, commit=True):
        photo = super().save(commit=commit)
        if commit:
            self._save_tags(photo)
        return photo

    def _save_tags(self, photo):
        raw_tags = self.cleaned_data.get("tags", "")
        tag_names = [t.strip() for t in raw_tags.split(",") if t.strip()]
        tags = []
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name__iexact=name, defaults={"name": name})
            tags.append(tag)
        photo.tags.set(tags)