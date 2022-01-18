from django.urls import path
from .views import photos, photoDetail, photoEdit, photoCreate, photoDelete, registerPage, loginPage, userAccount, updateProfile, logoutUser

urlpatterns = [
    path('detail/<int:pk>/', photoDetail, name='photo_detail'),
    path('edit/<int:pk>/', photoEdit, name='photo_edit'),
    path('add/', photoCreate, name='photo_create'),
    path('delete/<int:pk>/', photoDelete, name='photo_delete'),
    path('login/', loginPage, name='login'),
    path('register/', registerPage, name='register'),
    path('account/', userAccount, name='account'),
    path('update_profile/', updateProfile, name='update_profile'),
    path('logout/', logoutUser, name="logout"),

    path('', photos, name='list_photos'),
]
