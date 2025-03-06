from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.db.models import Count, F
from .models import Team, Match, Player, Goal, PlayerTeamHistory
from .forms import GoalForm

# Pagina Inicial
def home(request):
    """Página inicial com estatísticas do campeonato"""
    
    # 1️⃣ 10 artilheiros do campeonato
    top_scorers = Player.objects.annotate(total_goals=Count("scored_goals")).order_by("-total_goals")[:10]

    # 2️⃣ 10 jogadores com mais assistências
    top_assistants = Player.objects.annotate(total_assists=Count("assisted_goals")).order_by("-total_assists")[:10]

   # 3️⃣ Jogadores com mais participação em gols (Gols + Assistências)
    top_participation = Player.objects.annotate(
        total_goals=Count("scored_goals", distinct=True),
        total_assists=Count("assisted_goals", distinct=True)
    ).annotate(
        total_participation=F("total_goals") + F("total_assists")  # ✅ Agora está correto
    ).order_by("-total_participation")[:10]
    
    # 4️⃣ Próximos 10 jogos (partidas ainda não jogadas - `status=0`)
    upcoming_matches = Match.objects.filter(status=0).order_by("date")[:10]

    context = {
        "top_scorers": top_scorers,
        "top_assistants": top_assistants,
        "top_participation": top_participation,
        "upcoming_matches": upcoming_matches,
    }

    return render(request, "core/home.html", context)

# Registro de Usuario
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

# Lista de times
class TeamListView(ListView):
    model = Team
    template_name = "core/team/team_list.html"
    context_object_name = "teams"

# Detalhes de um time
class TeamDetailView(DetailView):
    model = Team
    template_name = "core/team/team_detail.html"
    context_object_name = "team"

# Criar um novo time (exige login)
class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    template_name = "core/team/team_form.html"
    fields = ["name", "acronym", "state", "emblem"]
    success_url = reverse_lazy("team_list")

# Editar um time existente (exige login)
class TeamUpdateView(LoginRequiredMixin, UpdateView):
    model = Team
    template_name = "core/team/team_form.html"
    fields = ["name", "acronym", "state", "emblem"]
    success_url = reverse_lazy("team_list")

# Deletar um time (exige login)
class TeamDeleteView(LoginRequiredMixin, DeleteView):
    model = Team
    template_name = "core/team/team_confirm_delete.html"
    success_url = reverse_lazy("team_list")

# Lista de partidas
class MatchListView(ListView):
    model = Match
    template_name = "core/match/match_list.html"
    context_object_name = "matches"
    paginate_by = 10

    def get_queryset(self):
        return Match.objects.all().order_by("round", "date", "id")  # Adiciona ID para ordenação consistente

# Detalhes de uma partida
class MatchDetailView(DetailView):
    model = Match
    template_name = "core/match/match_detail.html"
    context_object_name = "match"

# Criar uma nova partida (exige login)
class MatchCreateView(LoginRequiredMixin, CreateView):
    model = Match
    template_name = "core/match/match_form.html"
    fields = ["status", "round", "date", "hour", "stadium", "home_team", "visiting_team", "referee", "home_team_numgoals", "visiting_team_numgoals"]
    success_url = reverse_lazy("match_list")

# Editar uma partida existente (exige login)
class MatchUpdateView(LoginRequiredMixin, UpdateView):
    model = Match
    template_name = "core/match/match_form.html"
    fields = ["status", "round", "date", "hour", "stadium", "home_team", "visiting_team", "referee", "home_team_numgoals", "visiting_team_numgoals"]
    success_url = reverse_lazy("match_list")

# Deletar uma partida (exige login)
class MatchDeleteView(LoginRequiredMixin, DeleteView):
    model = Match
    template_name = "core/match/match_confirm_delete.html"
    success_url = reverse_lazy("match_list")

# Lista de jogadores
class PlayerListView(ListView):
    model = Player
    template_name = "core/player/player_list.html"
    context_object_name = "players"

# Detalhes de um jogador
class PlayerDetailView(DetailView):
    model = Player
    template_name = "core/player/player_detail.html"
    context_object_name = "player"

# Criar um novo jogador (exige login)
class PlayerCreateView(LoginRequiredMixin, CreateView):
    model = Player
    template_name = "core/player/player_form.html"
    fields = ["name", "number", "position", "age", "country"]
    success_url = reverse_lazy("player_list")

# Editar um jogador existente (exige login)
class PlayerUpdateView(LoginRequiredMixin, UpdateView):
    model = Player
    template_name = "core/player/player_form.html"
    fields = ["name", "number", "position", "age", "country"]
    success_url = reverse_lazy("player_list")

# Deletar um jogador (exige login)
class PlayerDeleteView(LoginRequiredMixin, DeleteView):
    model = Player
    template_name = "core/player/player_confirm_delete.html"
    success_url = reverse_lazy("player_list")

# Lista de Gols
class GoalListView(ListView):
    model = Goal
    template_name = "core/goal/goal_list.html"
    context_object_name = "goals"

# Detalhes de um gol
class GoalDetailView(DetailView):
    model = Goal
    template_name = "core/goal/goal_detail.html"
    context_object_name = "goal"

# Criar um novo gol (exige login)
class GoalCreateView(LoginRequiredMixin, CreateView):
    model = Goal
    form_class = GoalForm
    template_name = "core/goal/goal_form.html"
    #fields = ["match", "minute", "own_goal", "kicker", "assistant", "move", "shot_type", "goal_zone", "assist_type"]
    success_url = reverse_lazy("goal_list")

# Editar um gol existente (exige login)
class GoalUpdateView(LoginRequiredMixin, UpdateView):
    model = Goal
    template_name = "core/goal/goal_form.html"
    fields = ["match", "minute", "own_goal", "kicker", "assistant", "move", "shot_type", "goal_zone", "assist_type"]
    success_url = reverse_lazy("goal_list")

# Deletar um gol (exige login)
class GoalDeleteView(LoginRequiredMixin, DeleteView):
    model = Goal
    template_name = "core/goal/goal_confirm_delete.html"
    success_url = reverse_lazy("goal_list")

# Lista de Relacionamento Time-Jogador
class PlayerTeamHistoryListView(ListView):
    model = PlayerTeamHistory
    template_name = "core/playerteamhistory/playerteamhistory_list.html"
    context_object_name = "playerteamhistories"

# Detalhes de um relacionamento time-jogador
class PlayerTeamHistoryDetailView(DetailView):
    model = PlayerTeamHistory
    template_name = "core/playerteamhistory/playerteamhistory_detail.html"
    context_object_name = "playerteamhistory"

# Criar um novo relacionamento time-jogador (exige login)
class PlayerTeamHistoryCreateView(LoginRequiredMixin, CreateView):
    model = PlayerTeamHistory
    template_name = "core/playerteamhistory/playerteamhistory_form.html"
    fields = ["player", "team", "start_date"]
    success_url = reverse_lazy("playerteamhistory_list")

# Editar um relacionamento time-jogador existente (exige login)
class PlayerTeamHistoryUpdateView(LoginRequiredMixin, UpdateView):
    model = PlayerTeamHistory
    template_name = "core/playerteamhistory/playerteamhistory_form.html"
    fields = ["player", "team", "start_date"]
    success_url = reverse_lazy("playerteamhistory_list")

# Deletar um relacionamento time-jogador (exige login)
class PlayerTeamHistoryDeleteView(LoginRequiredMixin, DeleteView):
    model = PlayerTeamHistory
    template_name = "core/playerteamhistory/playerteamhistory_confirm_delete.html"
    success_url = reverse_lazy("playerteamhistory_list")
