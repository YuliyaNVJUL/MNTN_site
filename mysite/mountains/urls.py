from django.template.context_processors import i18n
from django.urls import path, include

from .views import main_page, UserLoginView, profile, UserLogoutview, ChangeUserInfoView, UserPasswordChangeView, \
    registration, all_categories, subcategories, subcategory_equipment, detail_equipment, all_posts, post_details, \
    wish_remove, send_tele

app_name = 'mountains'

urlpatterns = [
    path('', main_page, name='main_page'),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/password/change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/registration/', registration, name='registration'),
    path('accounts/logout/', UserLogoutview.as_view(), name='logout'),
    path('all_categories/', all_categories, name='all_categories'),
    path('subcategories/<int:pk>/', subcategories, name='subcategories'),
    path('subcategory_equipment/<int:pk>/', subcategory_equipment, name='subcategory_equipment'),
    path('detail_equipment/<int:pk>/', detail_equipment, name='detail_equipment'),
    path('all_posts/', all_posts, name='all_posts'),
    path('post_details/<int:pk>/', post_details, name='post_details'),
    path('remove/', wish_remove, name='wish_remove'),
    path('send_tele/', send_tele, name='send_tele'),
]
