from django.urls import path, include
from .views import (
    user_login, user_logout, register,
    profile, create_request, delete_request,
    update_request_status, add_category, delete_category,
    manage_categories)
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = ([
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('create-request/', create_request, name='create_request'),
    path('delete_request/<int:request_id>/', delete_request, name='delete_request'),
    path('update_request_status/<int:request_id>/', update_request_status, name='update_request_status'),
    path('manage-categories/', manage_categories, name='manage_categories'),
    path('add-category/', add_category, name='add_category'),
    path('delete-category/<int:category_id>/', delete_category, name='delete_category'),
]
               + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))