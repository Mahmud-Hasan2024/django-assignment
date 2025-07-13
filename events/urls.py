from django.urls import path
from events.views import dashboard_view, EventListView, EventDetailView, EventCreateView, EventUpdateView, EventDeleteView, ParticipantListView, ParticipantDetailView, ParticipantCreateView, ParticipantUpdateView, ParticipantDeleteView, CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, manage_groups, manage_users, create_user, create_group, delete_group, delete_user, assign_role, no_permission, edit_user, edit_group, rsvp_list, rsvp_event

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    
    path('event/', EventListView.as_view(), name='event_list'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('event/create/', EventCreateView.as_view(), name='create_event'),
    path('event/<int:pk>/update/', EventUpdateView.as_view(), name='update_event'),
    path('event/<int:pk>/delete/', EventDeleteView.as_view(), name='delete_event'),

    path('participant/', ParticipantListView.as_view(), name='participant_list'),
    path('participant/<int:pk>/', ParticipantDetailView.as_view(), name='participant_detail'),
    path('participant/create/', ParticipantCreateView.as_view(), name='create_participant'),
    path('participant/<int:pk>/update/', ParticipantUpdateView.as_view(), name='update_participant'),
    path('participant/<int:pk>/delete/', ParticipantDeleteView.as_view(), name='delete_participant'),

    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('category/create/', CategoryCreateView.as_view(), name='create_category'),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view(), name='update_category'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='delete_category'),

    path('manage-users/', manage_users, name='manage_users'),
    path('assign-role/<int:user_id>/', assign_role, name='assign_role'),
    path('create-user/', create_user, name='create_user'),
    path('users/<int:user_id>/edit/', edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),

    path('create-group/', create_group, name='create_group'),
    path('groups/<int:group_id>/permissions/', edit_group, name='edit_group'),
    path('manage-groups/', manage_groups, name='manage_groups'),
    path('delete-group/<int:group_id>/', delete_group, name='delete_group'),

    path('events/<int:event_id>/rsvp/', rsvp_event, name='rsvp_event'),
    path('rsvp-list/', rsvp_list, name='rsvp_list'),

    path('no-permission/', no_permission, name='no-permission'),
]