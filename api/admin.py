from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Hobby, FriendRequests

admin.site.register(User, UserAdmin)
admin.site.register(Hobby)
admin.site.register(FriendRequests)
