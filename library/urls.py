from django.urls import path
from .views import *

urlpatterns = [
    path('example', example),
    path('author-register', author_registration, name='author-register'),
    path('login', loginview, name='login'),
    path('logout', signout, name='logout'),
    path('add-book', add_book, name='add-book'),
    path('success/<str:message>', success, name='success'),
    path('fail/<str:message>', fail, name='fail'),
    path('mybooks', mybooks, name='mybooks'),
    path('mybooks/<str:pk>', edit_book, name='edit_book'),
    path('delete-book/<str:pk>', delete_book, name='delete_book'),
    path('profile', profile, name='profile'),
    path('change-password', change_password, name='change_password'),


]