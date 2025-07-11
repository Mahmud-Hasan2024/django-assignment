from django.urls import path
from events.views import dashboard_view, event_list, event_detail, create_event, update_event, delete_event, participant_list, participant_detail, create_participant, update_participant, delete_participant, category_list, category_detail, create_category, update_category, delete_category, manage_groups, manage_users, create_user, create_group, delete_group, delete_user, assign_role, no_permission, edit_user, edit_group, rsvp_list, rsvp_event

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    
    path('event/', event_list, name='event_list'),
    path('event/<int:event_id>/', event_detail, name='event_detail'),
    path('event/create/', create_event, name='create_event'),
    path('event/<int:event_id>/update/', update_event, name='update_event'),
    path('event/<int:event_id>/delete/', delete_event, name='delete_event'),

    path('participant/', participant_list, name='participant_list'),
    path('participant/<int:participant_id>/', participant_detail, name='participant_detail'),
    path('participant/create/', create_participant, name='create_participant'),
    path('participant/<int:participant_id>/update/', update_participant, name='update_participant'),
    path('participant/<int:participant_id>/delete/', delete_participant, name='delete_participant'),

    path('category/', category_list, name='category_list'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),
    path('category/create/', create_category, name='create_category'),
    path('category/<int:category_id>/update/', update_category, name='update_category'),
    path('category/<int:category_id>/delete/', delete_category, name='delete_category'),

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