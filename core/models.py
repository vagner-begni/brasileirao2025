from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=20)
    acronym = models.CharField(max_length=2)

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=20)
    acronym = models.CharField(max_length=2)

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=20)
    acronym = models.CharField(max_length=2)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=30)
    acronym = models.CharField(max_length=3)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    emblem = models.ImageField(upload_to="team_emblems/", null=True, blank=True)

    def __str__(self):
        return self.name

class Stadium(models.Model):
    name = models.CharField(max_length=40)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Referee(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(max_length=20)
    acronym = models.CharField(max_length=2)

    def __str__(self):
        return self.name

class Move(models.Model):
    name = models.CharField(max_length=20)
    acronym = models.CharField(max_length=2)

    def __str__(self):
        return self.name

class ShotType(models.Model):
    name = models.CharField(max_length=20)
    acronym = models.CharField(max_length=2)

    def __str__(self):
        return self.name

class GoalZone(models.Model):
    name = models.CharField(max_length=20)
    acronym = models.CharField(max_length=2)

    def __str__(self):
        return self.name

class AssistType(models.Model):
    name = models.CharField(max_length=30)
    acronym = models.CharField(max_length=2)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_current_team(self):
        latest_team = self.teams.order_by('-start_date').first()
        return latest_team.team if latest_team else None

class PlayerTeamHistory(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="teams")
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    start_date = models.DateField()

    def __str__(self):
        return f"{self.player.name} - {self.team.name} ({self.start_date})"

class Match(models.Model):
    status = models.IntegerField(default=0)
    round = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    hour = models.TimeField(null=True, blank=True)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home_matches")
    visiting_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="visiting_matches")
    referee = models.ForeignKey(Referee, on_delete=models.CASCADE)
    home_team_numgoals = models.IntegerField(default=0)
    visiting_team_numgoals = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.home_team} x {self.visiting_team} ({self.date})"

class Goal(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    minute = models.IntegerField(null=True, blank=True)
    own_goal = models.BooleanField(default=False)
    kicker = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="scored_goals")
    assistant = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True, related_name="assisted_goals")
    move = models.ForeignKey(Move, on_delete=models.CASCADE)
    shot_type = models.ForeignKey(ShotType, on_delete=models.SET_NULL, null=True, blank=True)
    goal_zone = models.ForeignKey(GoalZone, on_delete=models.SET_NULL, null=True, blank=True)
    assist_type = models.ForeignKey(AssistType, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        """Atualiza o placar da partida ao adicionar um gol"""
        is_new = self.pk is None  # Verifica se é um novo gol ou uma atualização
        super().save(*args, **kwargs)
        
        if is_new:
            if self.own_goal:
                if self.kicker.get_current_team() == self.match.visiting_team:
                    self.match.home_team_numgoals += 1
                elif self.kicker.get_current_team() == self.match.home_team:
                    self.match.visiting_team_numgoals += 1
            else:
                if self.kicker.get_current_team() == self.match.home_team:
                    self.match.home_team_numgoals += 1
                elif self.kicker.get_current_team() == self.match.visiting_team:
                    self.match.visiting_team_numgoals += 1
        
            self.match.status = 1  # Se um gol foi registrado, a partida não está mais em 0
            self.match.save()

    def delete(self, *args, **kwargs):
        """Atualiza o placar da partida ao remover um gol"""
        if self.own_goal:
            if self.kicker.get_current_team() == self.match.visiting_team:
                self.match.home_team_numgoals -= 1
            elif self.kicker.get_current_team() == self.match.home_team:
                self.match.visiting_team_numgoals -= 1
        else:
            if self.kicker.get_current_team() == self.match.home_team:
                self.match.home_team_numgoals -= 1
            elif self.kicker.get_current_team() == self.match.visiting_team:
                self.match.visiting_team_numgoals -= 1

        self.match.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.kicker.name} - {self.match} aos {self.minute} min"
