from django.contrib import admin
from django.urls import path, include
from user import views as user_view
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


# Define app_name for both apps
app_name = 'dashboard'
user_app_name = 'user'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("dashboard.urls")),
    path('register/', user_view.register, name="user-register"),
    
    # Use as_view() for LoginView and LogoutView
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='user-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='user-logout'),
    path('profile/', user_view.profile, name="user-profile"),
    path('profile/update', user_view.profile_update, name="user-profile-update"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)