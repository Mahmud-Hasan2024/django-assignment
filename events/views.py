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
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.
def get_user_role(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.groups.filter(name='admin').exists():
            return 'admin'
        elif request.user.groups.filter(name='organizer').exists():
            return 'organizer'
        else:
            return 'participant'
    return None

# Class Based View ekhan theke Shuru korsi

class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        events = Event.objects.select_related('category').prefetch_related('participants')
        if query:
            events = events.filter(name__icontains=query)
        return events

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['user_role'] = get_user_role(self.request)
        return context


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = get_user_role(self.request)
        return context


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'create_event.html'
    success_url = reverse_lazy('event_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = get_user_role(self.request)
        return context


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'update_event.html'

    def get_success_url(self):
        return reverse_lazy('event_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = get_user_role(self.request)
        return context


class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'delete_event.html'
    success_url = reverse_lazy('event_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = get_user_role(self.request)
        return context


class ParticipantListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'participant_list.html'
    context_object_name = 'participants'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        users = User.objects.prefetch_related('events')
        if query:
            users = users.filter(username__icontains=query)
        return users

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['user_role'] = get_user_role(self.request)
        return context


class ParticipantDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'participant_detail.html'
    context_object_name = 'participant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = get_user_role(self.request)
        return context


class ParticipantCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = ParticipantCreationForm
    template_name = 'create_participant.html'
    success_url = reverse_lazy('participant_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = get_user_role(self.request.user)
        return context


class ParticipantUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ParticipantUpdateForm
    template_name = 'update_participant.html'

    def get_success_url(self):
        return reverse_lazy('participant_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = get_user_role(self.request)
        return context


class ParticipantDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'delete_participant.html'
    success_url = reverse_lazy('participant_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = get_user_role(self.request)
        return context


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Category.objects.filter(name__icontains=query)
        return Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['user_role'] = get_user_role(self.request)
        return context


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = get_user_role(self.request)
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'create_category.html'
    success_url = reverse_lazy('category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = get_user_role(self.request)
        return context


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'update_category.html'

    def get_success_url(self):
        return reverse_lazy('category_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = get_user_role(self.request)
        return context


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'delete_category.html'
    success_url = reverse_lazy('category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = get_user_role(self.request)
        return context
    

# Class Based View ekhane shesh korsi


@login_required
def dashboard_view(request):
    user = request.user
    user_role = None

    if user.is_superuser or user.groups.filter(name__iexact='admin').exists():
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