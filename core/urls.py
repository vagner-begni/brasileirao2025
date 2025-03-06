from django.urls import path, include
from .views import register, home
from .views import TeamListView, TeamDetailView, TeamCreateView, TeamUpdateView, TeamDeleteView
from .views import MatchListView, MatchDetailView, MatchCreateView, MatchUpdateView, MatchDeleteView
from .views import PlayerListView, PlayerDetailView, PlayerCreateView, PlayerUpdateView, PlayerDeleteView
from .views import GoalListView, GoalDetailView, GoalCreateView, GoalUpdateView, GoalDeleteView
from .views import PlayerTeamHistoryListView, PlayerTeamHistoryDetailView, PlayerTeamHistoryCreateView, PlayerTeamHistoryUpdateView, PlayerTeamHistoryDeleteView

urlpatterns = [
    path("", home, name="home"),  # Página inicial
    path('register/', register, name="register"),               # Adiciona URL de registro
    path("accounts/", include("django.contrib.auth.urls")),     # URLs padrão de login/logout
    
    path("teams/", TeamListView.as_view(), name="team_list"),
    path("teams/<int:pk>/", TeamDetailView.as_view(), name="team_detail"),
    path("teams/new/", TeamCreateView.as_view(), name="team_create"),
    path("teams/<int:pk>/edit/", TeamUpdateView.as_view(), name="team_edit"),
    path("teams/<int:pk>/delete/", TeamDeleteView.as_view(), name="team_delete"),

    path("matches/", MatchListView.as_view(), name="match_list"),
    path("matches/<int:pk>/", MatchDetailView.as_view(), name="match_detail"),
    path("matches/new/", MatchCreateView.as_view(), name="match_create"),
    path("matches/<int:pk>/edit/", MatchUpdateView.as_view(), name="match_edit"),
    path("matches/<int:pk>/delete/", MatchDeleteView.as_view(), name="match_delete"),

    path("players/", PlayerListView.as_view(), name="player_list"),
    path("players/<int:pk>/", PlayerDetailView.as_view(), name="player_detail"),
    path("players/new/", PlayerCreateView.as_view(), name="player_create"),
    path("players/<int:pk>/edit/", PlayerUpdateView.as_view(), name="player_edit"),
    path("players/<int:pk>/delete/", PlayerDeleteView.as_view(), name="player_delete"),

    path("goals/", GoalListView.as_view(), name="goal_list"),
    path("goals/<int:pk>/", GoalDetailView.as_view(), name="goal_detail"),
    path("goals/new/", GoalCreateView.as_view(), name="goal_create"),
    path("goals/<int:pk>/edit/", GoalUpdateView.as_view(), name="goal_edit"),
    path("goals/<int:pk>/delete/", GoalDeleteView.as_view(), name="goal_delete"),

    path("playerteamhistories/", PlayerTeamHistoryListView.as_view(), name="playerteamhistory_list"),
    path("playerteamhistories/<int:pk>/", PlayerTeamHistoryDetailView.as_view(), name="playerteamhistory_detail"),
    path("playerteamhistories/new/", PlayerTeamHistoryCreateView.as_view(), name="playerteamhistory_create"),
    path("playerteamhistories/<int:pk>/edit/", PlayerTeamHistoryUpdateView.as_view(), name="playerteamhistory_edit"),
    path("playerteamhistories/<int:pk>/delete/", PlayerTeamHistoryDeleteView.as_view(), name="playerteamhistory_delete"),
]