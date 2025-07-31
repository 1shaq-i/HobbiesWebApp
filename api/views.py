from datetime import date
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
import json
from django.urls import reverse
from .models import User, Hobby, FriendRequests
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.db.models import Q


class CustomUserCreationForm(UserCreationForm):
    """
    A custom user creation form that includes fields for date of birth and hobbies.
    """
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password1', 'password2', 'date_of_birth', 'hobbies'
        ]


class ProfileUpdateForm(forms.ModelForm):
    """
    A form for updating the user's profile, including optional fields for
    date of birth and hobbies.
    """
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'date_of_birth', 'hobbies']


@login_required(login_url='/login/')
def update_password(request: HttpRequest) -> JsonResponse:
    """
    Updates the user's password.
    
    Accepts a POST request containing the new password.
    Prevents logout after a successful password change.
    """
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)

        form = PasswordChangeForm(user, data)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)  # Keeps user logged in after password change
            return JsonResponse({
                "success": True,
                "message": "Password updated successfully."
            })
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=405)


@login_required(login_url='/login/')
def get_friends_list(request: HttpRequest) -> JsonResponse:
    """
    Retrieves the user's friends list.

    Accepts a GET request and returns the list of friends, 
    including their username, email, and hobbies.
    """
    if request.method == 'GET':
        user = request.user

        # Fetch the user's friends
        friends = user.friends_list.all()

        # Prepare response data
        response_data = [
            {
                'username': friend.username,
                'email': friend.email,
                'hobbies': list(friend.hobbies.values_list('name', flat=True)),
            }
            for friend in friends
        ]

        return JsonResponse({'friends': response_data}, status=200)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


@login_required(login_url='/login/')
def get_profile_data(request: HttpRequest) -> JsonResponse:
    """
    Retrieves the profile data of the logged-in user.

    Accepts a GET request and returns the user's details, 
    including their hobbies as a list of tuples.
    """
    if request.method == 'GET':
        user = request.user

        profile_data = model_to_dict(
            user,
            fields=['username', 'email', 'first_name', 'last_name', 'date_of_birth']
        )
        profile_data['hobbies'] = list(user.hobbies.values_list('id', 'name'))
        
        return JsonResponse(profile_data)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


@login_required(login_url='/login/')
def update_profile_data(request: HttpRequest) -> JsonResponse:
    """
    Updates the profile data of the logged-in user.

    Accepts a POST request with the updated profile information.
    """
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)
        form = ProfileUpdateForm(data, instance=user)

        if form.is_valid():
            form.save()
            return JsonResponse({
                "success": True,
                "message": "Profile updated successfully."
            })
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=405)


@login_required(login_url='/login/')
def get_received_friend_requests(request: HttpRequest) -> JsonResponse:
    """
    Retrieves all incoming friend requests for the logged-in user.

    Accepts a GET request and returns the details of incoming friend requests.
    """
    if request.method == 'GET':
        user = request.user

        # Fetch all incoming friend requests
        incoming_requests = FriendRequests.objects.filter(receiver=user)

        # Prepare response data
        response_data = [
            {
                'id': request.id,
                'username': request.sender.username,
                'email': request.sender.email,
                'hobbies': list(request.sender.hobbies.values_list('name', flat=True)),
            }
            for request in incoming_requests
        ]

        return JsonResponse({'friend_requests': response_data}, status=200)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


@login_required(login_url='/login/')
def handle_friend_request(request: HttpRequest) -> JsonResponse:
    """
    Handles friend request actions (accept or decline).

    Accepts PUT or DELETE requests to handle the specified friend request ID.
    """
    if request.method in ['PUT', 'DELETE']:
        try:
            user = request.user
            data = json.loads(request.body)
            friend_request_id = data.get('id')

            if not friend_request_id:
                return JsonResponse({'error': 'Friend request ID is required.'}, status=400)

            friend_request = FriendRequests.objects.get(id=friend_request_id, receiver=user)

            if request.method == 'PUT':
                # Accept the friend request
                friend_request.sender.friends_list.add(user)
                user.friends_list.add(friend_request.sender)
                friend_request.delete()
                return JsonResponse({'message': 'Friend request accepted.'}, status=200)

            if request.method == 'DELETE':
                # Decline the friend request
                friend_request.delete()
                return JsonResponse({'message': 'Friend request declined.'}, status=200)

        except FriendRequests.DoesNotExist:
            return JsonResponse({'error': 'Friend request not found.'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


def is_authenticated(request: HttpRequest) -> JsonResponse:
    """
    Checks if the user is authenticated.

    Returns:
        - JsonResponse: {"authenticated": True} if authenticated.
        - JsonResponse: {"authenticated": False} with 401 status if not authenticated.
    """
    if request.user.is_authenticated:
        return JsonResponse({"authenticated": True})
    return JsonResponse({"authenticated": False}, status=401)


@login_required(login_url='/login/')
def csrf(request: HttpRequest) -> JsonResponse:
    """
    Retrieves the CSRF token for the current session.

    Returns:
        JsonResponse: Contains the CSRF token.
    """
    return JsonResponse({'csrfToken': get_token(request)})


def register(request: HttpRequest) -> HttpResponse:
    """
    Handles user registration.

    If the request method is POST, validates and saves the user. 
    Otherwise, displays the registration form.
    """
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('api:login')

    return render(request, 'registration/registration.html', {'form': form})


def login_api(request: HttpRequest) -> HttpResponse:
    """
    Handles user login.

    Accepts a POST request with username and password. If authenticated, logs
    the user in and returns a redirect URL. Otherwise, returns an error.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({
                'redirect_url': '/profile/'
            })
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

    return render(request, 'registration/login.html')


def logout_api(request: HttpRequest) -> HttpResponse:
    """
    Logs the user out and redirects to the login page.
    """
    logout(request)
    return redirect('api:login')


def calculate_age(dob: date) -> int:
    """
    Calculates a user's age based on their date of birth.

    Args:
        dob (date): The user's date of birth.

    Returns:
        int: The user's age.
    """
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age


@login_required(login_url='/login/')
def user_similarity(request: HttpRequest) -> JsonResponse:
    """
    Retrieves a list of users similar to the current user based on shared hobbies.

    Users can be filtered by age range and paginated. Similarity is determined
    by the number of shared hobbies.
    """
    user = request.user
    user_hobbies = set(user.hobbies.values_list('id', flat=True))

    # Fetch age filters from request
    age_min = request.GET.get('age_min', None)
    age_max = request.GET.get('age_max', None)

    # Fetch all users sharing hobbies with the current user, excluding the user
    similar_users = User.objects.filter(hobbies__in=user_hobbies).exclude(id=user.id).distinct()

    # Apply age filter if provided
    if age_min is not None and age_max is not None:
        age_min, age_max = int(age_min), int(age_max)
        similar_users = [
            u for u in similar_users
            if age_min <= calculate_age(u.date_of_birth) <= age_max
        ]

    # Sort users by the number of shared hobbies (descending)
    similar_users = sorted(
        similar_users,
        key=lambda u: len(set(u.hobbies.values_list('id', flat=True)) & user_hobbies),
        reverse=True
    )

    # Paginate the results
    paginator = Paginator(similar_users, 10)  # 10 users per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Prepare response data
    response_data = [
        {
            'username': u.username,
            'email': u.email,
            'age': calculate_age(u.date_of_birth),
            'shared_hobbies': len(set(u.hobbies.values_list('id', flat=True)) & user_hobbies),
            'hobbies': list(u.hobbies.values_list('name', flat=True)),
        }
        for u in page_obj
    ]

    return JsonResponse({
        'users': response_data,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'page_number': page_obj.number,
        'total_pages': paginator.num_pages,
    })


@login_required(login_url='api:login')
def profile_page(request: HttpRequest) -> HttpResponse:
    """
    Displays and handles updates to the user's profile.

    GET: Renders the profile update page with the user's current data.
    POST: Updates the user's profile if the form is valid.
    """
    user = request.user

    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, instance=user)

        if profile_form.is_valid():
            profile_form.save()
            # Prevents logout after password change by updating the session
            update_session_auth_hash(request, user)
            return render(request, 'registration/profile_page.html', context={'profile_form': profile_form})
    else:
        profile_form = ProfileUpdateForm(instance=user)
    
    return render(request, 'registration/profile_page.html', context={'profile_form': profile_form})


@login_required(login_url='api:login')
def password_update_page(request: HttpRequest) -> HttpResponse:
    """
    Displays and handles updates to the user's password.

    GET: Renders the password update form.
    POST: Updates the user's password if the form is valid and keeps the session active.
    """
    user = request.user

    if request.method == 'POST':
        password_form = PasswordChangeForm(user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Prevent logout after password change
            return redirect('api:profile_page')

    password_form = PasswordChangeForm(user)
    return render(request, 'registration/password_update_page.html', {'password_form': password_form})


@login_required(login_url='/login/')
def hobbies_api(request: HttpRequest) -> JsonResponse:
    """
    Handles the hobbies API.

    GET: Returns a list of all hobbies.
    POST: Creates a new hobby and returns its data.
    """
    if request.method == 'GET':
        try:
            hobbies = Hobby.objects.all()
            hobbies_data = [{"id": hobby.id, "name": hobby.name} for hobby in hobbies]
            return JsonResponse(hobbies_data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)})

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            hobby = Hobby.objects.create(name=data['name'])
            hobby_data = {"id": hobby.id, "name": hobby.name}
            return JsonResponse(hobby_data)
        except Exception as e:
            return JsonResponse({"error": str(e)})
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)


@login_required(login_url='/login/')
def send_friend_request(request: HttpRequest) -> JsonResponse:
    """
    Handles sending friend requests.

    POST: Sends a friend request to the specified username if valid conditions are met.
    """
    if request.method == 'POST':
        try:
            user = request.user
            data = json.loads(request.body)
            username = data.get('username')

            if not username:
                return JsonResponse({"error": "Username is required."}, status=400)

            potential_friend = User.objects.get(username=username)

            if potential_friend in user.friends_list.all():
                return JsonResponse({"message": "You are already friends with this user."}, status=400)

            if FriendRequests.objects.filter(sender=user, receiver=potential_friend).exists():
                return JsonResponse({"message": "Friend request already sent."}, status=400)

            FriendRequests.objects.create(sender=user, receiver=potential_friend)
            return JsonResponse({"message": "Friend request sent successfully."}, status=200)

        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist."}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)


@login_required(login_url='/login/')
def friend_requests_received(request: HttpRequest) -> HttpResponse:
    """
    Handles displaying received friend requests and shared hobbies for the logged-in user.

    Retrieves the senders of friend requests and computes:
        - The count of shared hobbies between the user and each sender.
        - A list of hobbies for each sender.
    """
    user = request.user
    user_hobbies = set(user.hobbies.values_list('id', flat=True))
    friend_request_senders = FriendRequests.objects.filter(receiver=user).values_list('sender', flat=True)

    # Calculate shared hobbies count and hobbies list for each sender
    friend_request_info = [
        {
            'sender': User.objects.get(pk=sender_id),
            'shared_hobbies_count': len(user_hobbies & set(User.objects.get(pk=sender_id).hobbies.values_list('id', flat=True))),
            'hobbies': list(User.objects.get(pk=sender_id).hobbies.values_list('name', flat=True)),
        }
        for sender_id in friend_request_senders
    ]

    return render(request, 'registration/friend_requests_received.html', {'friend_request_info': friend_request_info})


@login_required(login_url='/login/')
def friend_request_accepter_deleter(request: HttpRequest) -> HttpResponse:
    """
    Accepts or deletes a friend request based on the HTTP method.

    PUT: Accepts the friend request and updates both users' friend lists.
    DELETE: Deletes the friend request without adding the user as a friend.
    """
    user = request.user
    data = json.loads(request.body)
    friend_name = data['username']

    try:
        friend_object = User.objects.get(username=friend_name)
        record = FriendRequests.objects.get(sender=friend_object, receiver=user)
        record.delete()

        # If the request is to accept the friend request
        if request.method == 'PUT':
            if friend_object in user.friends_list.all():
                return HttpResponse("You are already friends with this person!")
            user.friends_list.add(friend_object)
            friend_object.friends_list.add(user)
            return HttpResponse("Friend request accepted!")

        # If the request is to delete the friend request
        elif request.method == 'DELETE':
            return HttpResponse("Friend request deleted!")

        return HttpResponse("Invalid request method!")
    except ObjectDoesNotExist:
        return HttpResponse("Friend request or user does not exist!", status=404)


@login_required(login_url='/login/')
def edit_friends(request: HttpRequest) -> HttpResponse:
    """
    Handles removing friends from the user's friend list.

    DELETE: Removes the specified friend from both users' friend lists.
    GET: Renders a page listing the user's current friends.
    """
    user = request.user

    if request.method == 'DELETE':
        data = json.loads(request.body)
        friend_to_remove_username = data['username']

        try:
            friend_to_remove = User.objects.get(username=friend_to_remove_username)
            user.friends_list.remove(friend_to_remove)
            friend_to_remove.friends_list.remove(user)
            return HttpResponse("Friend removed!")
        except ObjectDoesNotExist:
            return HttpResponse("Friend not found!", status=404)

    return render(request, 'registration/edit_friends.html', {'friends': user.friends_list.all()})


@login_required(login_url='/login/')
def get_user_list_with_friend_flags(request: HttpRequest) -> JsonResponse:
    """
    Retrieves a list of all users excluding the current user, along with friendship and friend request statuses.

    The response includes:
        - Username, email, and age.
        - Hobbies.
        - Flags indicating if a friend request has been sent or if the user is already a friend.
    """
    current_user = request.user
    users = User.objects.exclude(id=current_user.id)
    response_data = [
        {
            'username': user.username,
            'email': user.email,
            'age': user.profile.age,  # Assuming age is stored in a related profile model
            'hobbies': list(user.hobbies.values_list('name', flat=True)),
            'friend_request_sent': FriendRequests.objects.filter(sender=current_user, receiver=user).exists(),
            'is_friend': user in current_user.friends_list.all(),
        }
        for user in users
    ]

    return JsonResponse({'users': response_data})


@login_required(login_url='/login/')
def delete_user(request: HttpRequest) -> JsonResponse:
    """
    Deletes the logged-in user from the database, along with their friend requests.

    DELETE: Deletes the user and all related friend requests, then redirects to the login page.
    """
    if request.method == 'DELETE':
        current_user = request.user

        try:
            # Delete the user and their friend requests
            current_user.delete()
            FriendRequests.objects.filter(sender=current_user).delete()
            FriendRequests.objects.filter(receiver=current_user).delete()
            return JsonResponse({"success": "Successfully deleted the user."}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Unable to delete user"}, status=404)

    return JsonResponse({"error": "Invalid request method."}, status=405)


@login_required(login_url='/login/')
def main_spa(request: HttpRequest) -> HttpResponse:
    """
    Renders the Single Page Application (SPA) entry point for the web application.
    """
    return render(request, 'api/spa/index.html', {})
