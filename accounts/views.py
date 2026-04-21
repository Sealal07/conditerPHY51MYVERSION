from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    return render(request, 'accounts/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def profile_view(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.phone = request.POST.get('phone', '')
        request.user.address = request.POST.get('address', '')
        request.user.save()
        return redirect('accounts:profile')
    return render(request, 'accounts/profile.html')