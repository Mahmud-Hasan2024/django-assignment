from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from users.forms import CreateUserForm, CustomLoginForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView
from users.forms import CustomLoginForm

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
    return render(request, 'registration/register.html', context)

class CustomLoginView(LoginView):
    form_class = CustomLoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()



def activate_user(request, user_id, token):
    user = User.objects.get(pk=user_id)
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated. You can now log in.")
        return redirect('login')
    else:
        return render(request, 'registration/activation_invalid.html')

