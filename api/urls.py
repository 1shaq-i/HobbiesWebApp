"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse

from .views import (main_spa, 
                    register, 
                    login_api, 
                    profile_page, 
                    logout_api, 
                    password_update_page, 
                    hobbies_api, 
                    user_similarity,
                    send_friend_request,
                    friend_requests_received,
                    friend_request_accepter_deleter,
                    edit_friends,
                    csrf,
                    is_authenticated,
                    get_profile_data,
                    update_profile_data,
                    update_password,
                    get_received_friend_requests,
                    handle_friend_request,
                    get_friends_list,
                    delete_user
                )

from .views import get_user_list_with_friend_flags


urlpatterns = [
    
    path('', main_spa, name='main_spa'),
    path('login/', login_api, name='login'),
    path('register/', register, name='register'),
    path('profile_page/', profile_page, name='profile_page'),
    path('logout/', logout_api, name='logout'),
    path('password_update/', password_update_page, name='password_change'),
    path('similar_hobbies/', user_similarity, name='similar_hobbies'),
    path('filtered_users/', user_similarity, name='filtered_users'),
    path('api/send_friend_request/', send_friend_request, name='send_friend_request'),
    path('api/hobbies/', hobbies_api, name='hobbies_api'),
    path('friend_requests_received/', friend_requests_received, name='friend_requests_received'),
    path('friend_request_accepter_deleter/', friend_request_accepter_deleter, name='friend_request_accepter_deleter'),
    path('edit_friends/', edit_friends, name='edit_friends'),
    path('csrf/', csrf, name='csrf'),
    path('api/authenticated/', is_authenticated, name='is_authenticated'),
    path('api/profile/', get_profile_data, name='get_profile_data'),
    path('api/profile/update/', update_profile_data, name='update_profile_data'),
    path('api/similar-users/', user_similarity, name='similar_users'),
    path('api/password/update/', update_password, name='update_password'),
    path('api/similar-users/', get_user_list_with_friend_flags, name='similar_users'),
    path('api/friend_requests/', get_received_friend_requests, name='get_received_friend_requests'),
    path('api/friend_requests/handle/', handle_friend_request, name='handle_friend_request'),
    path('api/friends_list/', get_friends_list, name='friends_list'),
    path('api/delete_user/', delete_user, name='delete_user')
]
