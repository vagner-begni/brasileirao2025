import os
import django
import sys

# Adicionar o diretório raiz do projeto ao PATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

# Configurar as configurações do Django corretamente
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brasileirao2025.settings")
django.setup()

import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from core.models import (
    Country, Region, State, Team, Stadium, Referee, Position, Move,
    ShotType, GoalZone, AssistType, Player, PlayerTeamHistory, Match, Goal
)
import os

def clear_database():
    print("Limpando o banco de dados...")

    # Apagar todas as dependências primeiro
    Goal.objects.all().delete()
    Match.objects.all().delete()
    PlayerTeamHistory.objects.all().delete()
    Player.objects.all().delete()
    AssistType.objects.all().delete()
    GoalZone.objects.all().delete()
    ShotType.objects.all().delete()
    Move.objects.all().delete()
    Position.objects.all().delete()
    Referee.objects.all().delete()
    Stadium.objects.all().delete()
    Team.objects.all().delete()
    State.objects.all().delete()
    Region.objects.all().delete()
    Country.objects.all().delete()

    print("Banco de dados limpo com sucesso!")

# Caminho do arquivo Excel
EXCEL_FILE_PATH = "tabelaBR2025.xlsx"

def import_countries(sheet_name="Country"):
    df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=sheet_name)
    for _, row in df.iterrows():
        Country.objects.get_or_create(id=row["id"], name=row["name"], acronym=row["acronym"])

def import_regions(sheet_name="Region"):
    df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=sheet_name)
    for _, row in df.iterrows():
        Region.objects.get_or_create(id=row["id"], name=row["name"], acronym=row["acronym"])

def import_states(sheet_name="State"):
    df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=sheet_name)
    for _, row in df.iterrows():
        region = Region.objects.get(id=row["region"])
        State.objects.get_or_create(id=row["id"], name=row["name"], acronym=row["acronym"], region=region)

def import_teams(sheet_name="Team"):
    df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=sheet_name)
    for _, row in df.iterrows():
        state = State.objects.get(id=row["state"])
        Team.objects.get_or_create(id=row["id"], name=row["name"], acronym=row["acronym"], state=state)

def import_stadiums(sheet_name="Stadium"):
    df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=sheet_name)
    for _, row in df.iterrows():
        state = State.objects.get(id=row["state"])
        Stadium.objects.get_or_create(id=row["id"], name=row["name"], state=state)

def import_referees(sheet_name="Referee"):
    df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=sheet_name)
    for _, row in df.iterrows():
        Referee.objects.get_or_create(id=row["id"], name=row["name"])

def import_positions(sheet_name="Position"):
    df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=sheet_name)
    for _, row in df.iterrows():
        Position.objects.get_or_create(id=row["id"], name=row["name"], acronym=row["acronym"])

def import_moves(sheet_name="Move"):
    df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=sheet_name)
    for _, row in df.iterrows():
        Move.objects.get_or_create(id=row["id"], name=row["name"], acronym=row["acronym"])

def import_shot_types(sheet_name="ShotType"):
    df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=sheet_name)
    for _, row in df.iterrows():
        ShotType.objects.get_or_create(id=row["id"], name=row["name"], acronym=row["acronym"])

def import_goal_zones(sheet_name="GoalZone"):
    df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=sheet_name)
    for _, row in df.iterrows():
        GoalZone.objects.get_or_create(id=row["id"], name=row["name"], acronym=row["acronym"])

def import_assist_types(sheet_name="AssistType"):
    df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=sheet_name)
    for _, row in df.iterrows():
        AssistType.objects.get_or_create(id=row["id"], name=row["name"], acronym=row["acronym"])

def import_players(sheet_name="Player"):
    df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=sheet_name)
    for _, row in df.iterrows():
        country = Country.objects.get(id=row["country"])
        position = Position.objects.get(id=row["position"])
        Player.objects.get_or_create(
            id=row["id"],
            name=row["name"],
            number=row.get("number"),
            position=position,
            age=row["age"],
            country=country,
        )

def import_player_team_history(sheet_name="PlayerTeamHistory"):
    df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=sheet_name)
    for _, row in df.iterrows():
        player = Player.objects.get(id=row["player"])
        team = Team.objects.get(id=row["team"])
        PlayerTeamHistory.objects.get_or_create(
            player=player,
            team=team,
            start_date=row["start_date"]
        )

def import_matches(sheet_name="Match"):
    df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=sheet_name)
    for _, row in df.iterrows():
        stadium = Stadium.objects.get(id=row["stadium"])
        home_team = Team.objects.get(id=row["home_team"])
        visiting_team = Team.objects.get(id=row["visiting_team"])
        referee = Referee.objects.get(id=row["referee"])
        Match.objects.get_or_create(
            id=row["id"],
            status=row["status"],
            round=row["round"],
            date=row["date"],
            hour=row["hour"],
            stadium=stadium,
            home_team=home_team,
            visiting_team=visiting_team,
            referee=referee,
            home_team_numgoals=row.get("home_team_numgoals", 0),
            visiting_team_numgoals=row.get("visiting_team_numgoals", 0),
        )

def import_goals(sheet_name="Goal"):
    df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=sheet_name)
    for _, row in df.iterrows():
        match = Match.objects.get(id=row["match"])
        kicker = Player.objects.get(id=row["kicker"])
        assistant = Player.objects.get(id=row["assistant"]) if not pd.isna(row["assistant"]) else None
        move = Move.objects.get(id=row["move"])
        shot_type = ShotType.objects.get(id=row["shot_type"])
        goal_zone = GoalZone.objects.get(id=row["goal_zone"])
        assist_type = AssistType.objects.get(id=row["assist_type"])
        Goal.objects.create(
            match=match,
            minute=row["minute"],
            own_goal=True if row["own?"] == "Sim" else False,
            kicker=kicker,
            assistant=assistant,
            move=move,
            shot_type=shot_type,
            goal_zone=goal_zone,
            assist_type=assist_type
        )

def run_import():
    print("Importando dados do Excel para o banco de dados...")
    # Limpa o banco de dados antes da importação
    clear_database()
    # Limpa o banco de dados antes da importação
    import_countries()
    import_regions()
    import_states()
    import_teams()
    import_stadiums()
    import_referees()
    import_positions()
    import_moves()
    import_shot_types()
    import_goal_zones()
    import_assist_types()
    import_players()
    import_player_team_history()
    import_matches()
    import_goals()
    print("Importação concluída!")

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brasileirao2025.settings")
    import django
    django.setup()
    run_import()
