# Photo Gallery

A full-stack photo gallery web application built with **Django**. Users can register, upload and tag photos, browse a searchable gallery, view photo details, and like/dislike photos. Images are stored on **Cloudinary** in production, with a clean **Tailwind CSS** interface throughout.

## Features

- **User accounts** — registration, login/logout, and password change
- **Profiles** — bio and avatar for every user, created automatically on sign-up
- **Photo uploads** — title, description, image, and comma-separated tags
- **Gallery browsing** — paginated grid with search (title/description) and tag filtering
- **Photo detail view** — full-size image with metadata
- **Likes / dislikes** — one reaction per user per photo, toggleable via AJAX or standard form post
- **Ownership & permissions** — only the uploader or staff can delete a photo
- **Admin panel** — manage photos, tags, likes, and profiles from Django admin
- **Cloud-ready storage** — Cloudinary for media, WhiteNoise for compressed static files

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2 (Python) |
| Database | PostgreSQL (via `dj-database-url`), SQLite for local dev |
| Media storage | Cloudinary (`django-cloudinary-storage`) |
| Static files | WhiteNoise |
| Frontend | Django Templates + Tailwind CSS (CDN) |
| Server | Gunicorn |

## Project Structure

```
Photo-gallery/
├── manage.py
├── requirements.txt
├── photogallery_project/       # Django project settings & root URLs
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── photo_gallery/               # Main application
│   ├── models.py                # Photo, Tag, Like, Profile
│   ├── views.py                 # Auth, gallery, upload, reactions
│   ├── forms.py                 # Styled auth & photo forms
│   ├── urls.py
│   ├── admin.py
│   ├── signals.py               # Auto-create Profile on user creation
│   ├── migrations/
│   └── templates/               # base.html + app templates
└── photos/                      # Local media directory
```

## Getting Started

### Prerequisites

- Python 3.10+
- pip
- A PostgreSQL database (optional locally — SQLite works if `DATABASE_URL` is unset)
- A [Cloudinary](https://cloudinary.com/) account (for image storage)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/JeromeJason-dev/Photo-gallery.git
   cd Photo-gallery
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   DATABASE_URL=postgres://user:password@localhost:5432/photogallery
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   ```

5. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser** (to access the admin panel)
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. Visit **http://127.0.0.1:8000/** in your browser 

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `SECRET_KEY` | Django secret key | Recommended |
| `DEBUG` | `True`/`False` — enable debug mode | No (defaults to `False`) |
| `DATABASE_URL` | Database connection string | Recommended for production |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name | Yes (for media uploads) |
| `CLOUDINARY_API_KEY` | Cloudinary API key | Yes |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | Yes |

## Main Routes

| URL | Description |
|---|---|
| `/` | Home / gallery listing |
| `/gallery/` | Gallery listing (alias of home) |
| `/photo/<id>/` | Photo detail view |
| `/photo/upload/` | Upload a new photo (login required) |
| `/photo/<id>/delete/` | Delete a photo (owner/staff only) |
| `/photo/<id>/react/<like\|dislike>/` | Like or dislike a photo |
| `/register/`, `/login/`, `/logout/` | Authentication |
| `/profile/`, `/profile/edit/` | User profile |
| `/admin/` | Django admin panel |


## Deployment

The project is configured for platforms like **Render**, **Railway**, or **Heroku**:

- `gunicorn` serves the WSGI application (`photogallery_project.wsgi`)
- `whitenoise` serves compressed static files without a separate static host
- `dj-database-url` parses the `DATABASE_URL` environment variable
- Media files are offloaded to Cloudinary, so no persistent disk is required

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.