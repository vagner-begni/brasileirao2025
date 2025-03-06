from django.contrib import admin
from .models import (
    Country, Region, State, Team, Stadium, Referee, Position,
    Move, ShotType, GoalZone, AssistType, Player, PlayerTeamHistory,
    Match, Goal
)

admin.site.register(Country)
admin.site.register(Region)
admin.site.register(State)
admin.site.register(Team)
admin.site.register(Stadium)
admin.site.register(Referee)
admin.site.register(Position)
admin.site.register(Move)
admin.site.register(ShotType)
admin.site.register(GoalZone)
admin.site.register(AssistType)
admin.site.register(Player)
admin.site.register(PlayerTeamHistory)
admin.site.register(Match)
admin.site.register(Goal)
