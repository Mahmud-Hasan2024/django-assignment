from django.shortcuts import render

# Create your views here.
def home(request):
    user = request.user

    if user.is_superuser or user.groups.filter(name__iexact='admin').exists():
        user_role = 'admin'
    elif user.groups.filter(name__iexact='organizer').exists():
        user_role = 'organizer'
    elif user.groups.filter(name__iexact='participant').exists():
        user_role = 'participant'
    else:
        user_role = None

    context = {
        'user_role': user_role,
    }
    return render(request, 'home.html', context)

def no_permission(request):
    return render(request, 'no_permission.html')
