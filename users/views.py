from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from users.forms import CreateUserForm, CustomLoginForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User, Group

# Create your views here.
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()

            participant_group, created = Group.objects.get_or_create(name='participant')
            user.groups.add(participant_group)

            messages.success(request, 'A Confirmation mail sent. Please check your email')
            return redirect('login')

    context = {'form' : form}
    return render(request, 'registrations/register.html', context)

def sign_in(request):
    form = CustomLoginForm()
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'registrations/login.html', {'form': form})


def sign_out(request):
    logout(request)
    return redirect('login')


def activate_user(request, user_id, token):
    user = User.objects.get(pk=user_id)
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated. You can now log in.")
        return redirect('login')
    else:
        return render(request, 'registrations/activation_invalid.html')

