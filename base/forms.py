from django.forms import ModelForm
from .models import Question, MatchingTeacher

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['topic','subtopic','title','body']
        
class MatchingForm(ModelForm):
    class Meta:
        model = MatchingTeacher
        fields = '__all__'
        exclude = ['user']