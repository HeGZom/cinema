from django.urls import path
from . import views

app_name = 'cinema'

urlpatterns = [
    # Маршруты для статических данных
    path('', views.index, name='index'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', views.category_posts, name='category_posts'),

    # Маршруты для работы с сеансами и бронированиями
    path('sessions/', views.SessionListView.as_view(), name='session_list'),
    path('sessions/<int:session_id>/', views.SessionDetailView.as_view(), name='session_detail'),
    path('reservation/<int:pk>/update/', views.update_reservation_status, name='update_reservation_status'),

    # Маршруты для администратора
    path('add_movie/', views.add_movie, name='add_movie'),
    path('add_session/', views.add_session, name='add_session'),

    # Маршруты для профиля пользователя
    path('profile/<int:pk>/edit/', views.ProfileUpdateView.as_view(), name='edit_profile'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
]