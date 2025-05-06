from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('create/', views.book_create, name='book_create'),
    path('offer/<int:book_id>/', views.offer_create, name='offer_create'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('add/', views.add_book, name='add_book'),
    path('exchange/<int:offered_book_id>/', views.create_exchange_request, name='create_exchange'),
    path('my-exchanges/', views.my_exchanges, name='my_exchanges'),
    path('offer/<int:offer_id>/accept/', views.update_offer_status, {'status': 'accepted'}, name='accept_offer'),
    path('offer/<int:offer_id>/reject/', views.update_offer_status, {'status': 'rejected'}, name='reject_offer'),
    path('book/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('book/<int:book_id>/delete/', views.delete_book, name='delete_book'),
]
