from django.forms import ModelForm
from .models import Question
from django import forms
from .models import Question, Matching

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['topic','title','body']


# class AddressForm(forms.Form):
#     subtopic = forms.ChoiceField(
#         choices = get_topic(),
#         required = False,
#         label='トピック',
#         widget=forms.Select(attrs={'class':'form-control','id':'id_topic'}),
#     )
        
class MatchingForm(ModelForm):
    class Meta:
        model = Matching
        fields = '__all__'
        exclude = ['user']
