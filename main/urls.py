from django.urls import path
from . import views
from .views import Home,Tournaments,teamDetails,matchCreate,tournamentCreate,tournamentUpdate,userDetails,teamCreate, matchUpdate,matchDelete,serverDetails,searchTournament


urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('tournaments/',Tournaments.as_view(),name='tournaments'),
    path('team/<int:pk>/',teamDetails.as_view(),name='team'),
    path('tournament/new/',tournamentCreate.as_view(),name='tournament-new'),
    path('tournament/<int:pk>/',views.tournamentDetails.as_view(),name='tournament'),
    path('tournament/<int:pk>/update/',views.tournamentUpdate.as_view(),name='tournament_update'),
    path('tournament/<int:id>/match/new/',matchCreate.as_view(),name = 'new_match'),
    path('tournament/<int:id>/match/<int:pk>/delete/',matchDelete.as_view(),name = 'delete_match'),
    path('user/<int:pk>/',userDetails.as_view(),name='user'),
    path('team/new/',teamCreate.as_view(),name = 'new_team'),

    path('tournament/<int:pk>/register/',views.register,name = 'register'),
    path('tournament/<int:pk>/feat/',views.temp,name='feat'),
    path('tournament/<int:pk>/random_matches/',views.test,name='random_matches'),
    path('tournament/<int:pk>/feat/',views.temp,name='feat'),
    path('tournament/<int:id>/match/<int:pk>/update/',matchUpdate.as_view(),name = 'tournament_update_match'),
    path('server/<int:pk>/',serverDetails.as_view(),name= 'server'),
    path('server/<int:pk>/start/',serverDetails.Start,name='server-start'),
    path('server/<int:pk>/stop/',serverDetails.Stop,name='server-stop'),
    path('server/<int:pk>/launchcs/',serverDetails.LaunchCS,name='server-launchcs'),
    path('server/<int:pk>/stopcs/',serverDetails.StopCS,name='server-stopcs'),
    path('server/<int:pk>/command/',serverDetails.CommandCS,name='server-command'),
    path('search/',searchTournament.as_view(),name='search'),
    path('tournament/<int:pk>/get_servers/',views.get_servers,name='get_servers'),
    path('tournament/<int:pk>/match/<int:id>/set_winner/',views.set_winner,name='set_winner'),
    path('tournament/<int:pk>/first_matches/',views.FirstMatches,name='first_matches'),
    path('tournament/<int:pk>/next_round/',views.next_round,name='next_round'),
    path('tournament/<int:pk>/match/<int:id>/set_server/',views.set_server,name='set_server'),



]