from django import forms
from .models import Goal, Match

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ["match", "minute", "own_goal", "kicker", "assistant", "move", "shot_type", "goal_zone", "assist_type"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordena as partidas por rodada e data na combobox
        self.fields["match"].queryset = Match.objects.all().order_by("round", "date")
