from django.urls import path
from .views import *

app_name = "home"
urlpatterns = [
    # path('', comingsoon, name='comingsoon'),
    path("", home, name="home"),
    path("contact/", contact, name="contact"),
    path("about/", about, name="about"),
    path("events/", events, name="events"),
    path("events/<str:pk>/", event_details, name="event_details"),

    # Apply
    path(
        "events/<str:pk>/apply/", 
        apply__select_member, 
        name="apply"
    ),
    path(
        "events/<str:event_id>/apply/<str:member_id>/", 
        apply__select_team, 
        name="apply__select_team",
    ),
    path(
        "events/<str:event_id>/apply/<str:member_id>/<str:team_id>/", 
        apply__select_category, 
        name="apply__select_category"
    ),
    path(
        "events/<str:event_id>/apply/<str:member_id>/<str:team_id>/<str:category_id>/", 
        apply__select_subcategory, 
        name="apply__select_subcategory"
    ),
    path(
        "events/<str:event_id>/apply/<str:member_id>/<str:team_id>/<str:category_id>/<str:subcategory_id>/",
        apply__select_submember,
        name="apply__select_submember",
    ),

    # Manage
    path("events/<str:pk>/manage/", manage, name="manage"),
    path(
        "events/<int:event_id>/manage/download_id/<int:reg_member_id>/",
        downloadID,
        name="downloadID",
    ),
    path(
        "events/<str:event_id>/manage/delete/<str:reg_member_id>/",
        event_member_delete,
        name="delete_member",
    ),


    # Members
    path("events/<str:pk>/members/", event_teams, name="teams"),
    

    path(
        "events/<str:event_id>/teams/<str:reg_team_id>/",
        event_team_details,
        name="team_details",
    ),
    path(
        "events/<str:event_id>/manage/<str:reg_team_id>/",
        event_team_update,
        name="update_team",
    ),

    path("events/<str:pk>/players/", event_players, name="players"),

    path("events/<int:event_id>/results/", result_categories, name="result_categories"),
    path("events/<int:event_id>/results/<int:category_id>/", results, name="results"),
    path(
        "events/<int:event_id>/<int:team_id>/<int:player_id>/download-id/",
        downloadID,
        name="downloadID",
    ),
    path(
        "events/<int:event_id>/<int:team_id>/<int:player_id>/download-cert/",
        downloadCert,
        name="downloadCert",
    ),
]
