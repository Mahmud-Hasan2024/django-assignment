from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from events.models import Event, Category
from events.forms import EventForm, CategoryForm, ParticipantCreationForm, ParticipantUpdateForm, EditUserForm, GroupPermissionForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from events.models import Event, Category
from django.contrib.auth.models import Group, User
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.
def get_user_role(request):
    if request.user.is_authenticated or request.user.groups.filter(name='admin').exists():
        if request.user.is_superuser:
            return 'admin'
        elif request.user.groups.filter(name='organizer').exists():
            return 'organizer'
        else:
            return 'participant'
    return None

@login_required
def event_list(request):
    user_role = get_user_role(request)
    query = request.GET.get('q', '')
    events = Event.objects.select_related('category').prefetch_related('participants')
    if query:
        events = events.filter(name__icontains=query)
    return render(request, 'event_list.html', {'events': events, 'query': query, 'user_role': user_role})

@login_required
def event_detail(request, event_id):
    user_role = get_user_role(request)
    event = Event.objects.select_related('category').prefetch_related('participants').get(pk=event_id)
    return render(request, 'event_detail.html', {'event': event, 'user_role': user_role})

@login_required
def create_event(request):
    user_role = get_user_role(request)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form, 'user_role': user_role})

@login_required
def update_event(request, event_id):
    user_role = get_user_role(request)
    event = Event.objects.get(pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'update_event.html', {'form': form, 'user_role': user_role})

@login_required
def delete_event(request, event_id):
    user_role = get_user_role(request)
    event = Event.objects.get(pk=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'delete_event.html', {'event': event, 'user_role': user_role})

@login_required
def participant_list(request):
    user_role = get_user_role(request)
    query = request.GET.get('q', '')
    participants = User.objects.prefetch_related('events')
    if query:
        participants = participants.filter(username__icontains=query)
    return render(request, 'participant_list.html', {'participants': participants, 'query': query, 'user_role': user_role})

@login_required
def participant_detail(request, participant_id):
    user_role = get_user_role(request)
    participant = User.objects.prefetch_related('events').get(pk=participant_id)
    return render(request, 'participant_detail.html', {'participant': participant, 'user_role': user_role})

@login_required
def create_participant(request):
    user_role = get_user_role(request)
    if request.method == 'POST':
        form = ParticipantCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
    else:
        form = ParticipantCreationForm()
    return render(request, 'create_participant.html', {'form': form, 'user_role': user_role})

@login_required
def update_participant(request, participant_id):
    user_role = get_user_role(request)
    participant = User.objects.get(pk=participant_id)
    if request.method == 'POST':
        form = ParticipantUpdateForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('participant_detail', participant_id=participant.id)
    else:
        form = ParticipantUpdateForm(instance=participant)
    return render(request, 'update_participant.html', {'form': form, 'user_role': user_role})

@login_required
def delete_participant(request, participant_id):
    user_role = get_user_role(request)
    participant = User.objects.get(pk=participant_id)
    if request.method == 'POST':
        participant.delete()
        return redirect('participant_list')
    return render(request, 'delete_participant.html', {'participant': participant, 'user_role': user_role})

@login_required
def category_list(request):
    user_role = get_user_role(request)
    query = request.GET.get('q', '')
    categories = Category.objects.all()
    if query:
        categories = categories.filter(name__icontains=query)
    return render(request, 'category_list.html', {'categories': categories, 'query': query, 'user_role': user_role})

@login_required
def category_detail(request, category_id):
    user_role = get_user_role(request)
    category = Category.objects.prefetch_related('events').get(pk=category_id)
    return render(request, 'category_detail.html', {'category': category, 'user_role': user_role})

@login_required
def create_category(request):
    user_role = get_user_role(request)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'create_category.html', {'form': form, 'user_role': user_role})

@login_required
def update_category(request, category_id):
    user_role = get_user_role(request)
    category = Category.objects.get(pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_detail', category_id=category.id)
    else:
        form = CategoryForm(instance=category)
    return render(request, 'update_category.html', {'form': form, 'user_role': user_role})

@login_required
def delete_category(request, category_id):
    user_role = get_user_role(request)
    category = Category.objects.get(pk=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'delete_category.html', {'category': category, 'user_role': user_role})


@login_required
def dashboard_view(request):
    user = request.user
    user_role = None

    if user.is_superuser:
        user_role = 'admin'
        total_users = User.objects.count()
        total_events = Event.objects.count()
        total_groups = Group.objects.count()
        total_categories = Category.objects.count()
        context = {
            'user_role': user_role,
            'total_users': total_users,
            'total_events': total_events,
            'total_groups': total_groups,
            'total_categories': total_categories,
        }
        return render(request, 'admin_dashboard.html', context)

    elif user.groups.filter(name__iexact='Organizer').exists():
        user_role = 'organizer'
        total_events = Event.objects.count()
        upcoming_events = Event.objects.filter(date__gte=timezone.now()).count()
        past_events = Event.objects.filter(date__lt=timezone.now()).count()
        total_categories = Category.objects.count()
        context = {
            'user_role': user_role,
            'total_events': total_events,
            'upcoming_events': upcoming_events,
            'past_events': past_events,
            'total_categories': total_categories,
        }
        return render(request, 'organizer_dashboard.html', context)

    elif user.groups.filter(name__iexact='Participant').exists():
        user_role = 'participant'
        rsvp_events = Event.objects.filter(participants=user)
        context = {
            'user_role': user_role,
            'events': rsvp_events,
        }
        return render(request, 'participant_dashboard.html', context)

    else:
        context = {'user_role': user_role}
        return render(request, 'core/no-permission.html', context)
    

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='admin').exists()

@login_required
@user_passes_test(is_admin, login_url='no-permission')
def manage_users(request):
    user_role = get_user_role(request)
    users = User.objects.exclude(is_superuser=True)
    return render(request, 'manage_users.html', {'users': users, 'user_role': user_role})


@login_required
@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    groups = Group.objects.all()
    user_role = get_user_role(request)

    if request.method == 'POST':
        selected_group = request.POST.get('group')
        user.groups.clear()
        if selected_group:
            group = Group.objects.get(name=selected_group)
            user.groups.add(group)
        return redirect('manage_users')

    return render(request, 'assign_role.html', {'target_user': user, 'groups': groups, 'user_role': user_role})

@login_required
@user_passes_test(is_admin, login_url='no-permission')
def create_user(request):
    user_role = get_user_role(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        group_name = request.POST.get('group')

        if username and password:
            user = User.objects.create_user(username=username, email=email, password=password)
            if group_name:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
            return redirect('manage_users')

    groups = Group.objects.all()
    return render(request, 'create_user.html', {'groups': groups, 'user_role': user_role})

@login_required
@user_passes_test(is_admin, login_url='no-permission')
def edit_user(request, user_id):
    user_role = get_user_role(request)
    user_obj = User.objects.get(pk=user_id)

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user_obj)
        if form.is_valid():
            user = form.save(commit=False)
            group_name = form.cleaned_data.get('group')
            user.groups.clear()
            if group_name:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
            user.save()
            return redirect('manage_users')
    else:
        if user_obj.groups.exists():
            first_group = user_obj.groups.first()
            previous_group = first_group.name
        else:
            previous_group = ''

        form = EditUserForm(instance=user_obj, initial={'group': previous_group})

    if user_obj.groups.exists():
        current_group = user_obj.groups.first().name
    else:
        current_group = ''

    context = {
        'form': form,
        'user_role': user_role,
        'all_groups': Group.objects.all(),
        'current_group': current_group,
    }

    return render(request, 'edit_user.html', context)

@login_required
@user_passes_test(is_admin, login_url='no-permission')
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    if user != request.user:
        user.delete()
    return redirect('manage_users')


@login_required
@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    user_role = get_user_role(request)

    if request.method == 'POST':
        form = GroupPermissionForm(request.POST)
        if form.is_valid():
            group = form.save()
            return redirect('manage_groups')
    else:
        form = GroupPermissionForm()

    return render(request, 'create_group.html', {'form': form, 'user_role': user_role,})


@login_required
@user_passes_test(is_admin, login_url='no-permission')
def edit_group(request, group_id):
    group = Group.objects.get(id=group_id)
    user_role = get_user_role(request)

    if request.method == 'POST':
        form = GroupPermissionForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('manage_groups')
    else:
        form = GroupPermissionForm(instance=group)

    return render(request, 'edit_group.html', {'form': form,'group': group, 'user_role': user_role,})

@login_required
@user_passes_test(is_admin, login_url='no-permission')
def manage_groups(request):
    groups = Group.objects.all()
    user_role = get_user_role(request)
    return render(request, 'manage_groups.html', {'groups': groups, 'user_role': user_role})

@login_required
@user_passes_test(is_admin, login_url='no-permission')
def delete_group(request, group_id):
    group = Group.objects.get(id=group_id)
    group.delete()
    return redirect('manage_groups')


    
def is_participant(user):
    return user.groups.filter(name='participant').exists()

@login_required
@user_passes_test(is_participant, login_url='no-permission')
def rsvp_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user in event.participants.all():
        messages.info(request, "You have already RSVPed to this event.")
        
    else:
        event.participants.add(request.user)
        messages.success(request, f"You have successfully RSVPed to {event.name}.")

    return redirect('event_list')

@login_required
@user_passes_test(is_participant, login_url='no-permission')
def rsvp_list(request):
    events = request.user.events.all()
    return render(request, 'rsvp_list.html', {'events': events, 'user_role': get_user_role(request)})


def no_permission(request):
    user_role = get_user_role(request)
    return render(request, 'no-permission.html', {'user_role': user_role})
