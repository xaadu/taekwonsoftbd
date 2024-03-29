from django.urls import path
from .views import (
    dashboard,
    profile,
    create_event,
    events,
    event_details,
    update_event,
    delete_event,

    categories,
    create_category,
    update_category,
    delete_category,

    sub_categories,
    create_subcategory,
    update_subcategory,
    delete_subcategory,
)


app_name = 'host'
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
    path('events/', events, name='events'),
    path('events/create/', create_event, name='create_event'),
    path('events/<str:pk>/', event_details, name='event_details'),
    path('events/<str:event_id>/update/', update_event, name='update_event'),
    path('events/<str:event_id>/delete/', delete_event, name='delete_event'),

    
    # Categories
    path('events/<str:event_id>/categories/', categories, name='categories'),
    path(
        'events/<str:event_id>/categories/create/',
        create_category, name='create_category'
    ),
    path(
        'events/<str:event_id>/categories/<str:category_id>/',
        update_category, name='update_category'
    ),
    path(
        'events/<str:event_id>/categories/<str:category_id>/delete/',
        delete_category, name='delete_category'
    ),


    # Sub Categories
    path(
        'events/<str:event_id>/categories/<str:category_id>/subcategories/',
        sub_categories, name='sub_categories',
    ),
    path(
        'events/<str:event_id>/categories/<str:category_id>/subcategories/create/',
        create_subcategory, name='create_subcategory',
    ),
    path(
        'events/<str:event_id>/categories/<str:category_id>/subcategories/<str:subcategory_id>/update/',
        update_subcategory, name='update_subcategory',
    ),
    path(
        'events/<str:event_id>/categories/<str:category_id>/subcategories/<str:subcategory_id>/delete/',
        delete_subcategory, name='delete_subcategory',
    ),
]
