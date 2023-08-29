from django.forms import ModelForm
from .models import Question
from django import forms
import json
from .models import Question, MatchingTeacher

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['topic','subtopic','title','body']

def readjson(filepath):
    with open(filepath, "r", encoding="utf-8_sig") as fp:
        return json.load(fp)

def get_topic():
    """トピックを選択する"""
    filepath = './json/topic.json'
    all_data = readjson(filepath)
    topic = list(all_data.keys())
    all_topic = [('------','---トピックを選択---')]
    for topoic in topic:
        all_topic.append((topic,topic))
    return all_topic

def return_subtopic_by_topic(topic):
    """トピックを選択を取得"""
    filepath = './base/json/topic.json'
    all_data = readjson(filepath)
    #指定のトピックのサブトピックデータを取得
    all_subtopic = all_data[topic]
    return all_subtopic

class AddressForm(forms.Form):
    subtopic = forms.ChoiceField(
        choices = get_topic(),
        required = False,
        label='トピック',
        widget=forms.Select(attrs={'class':'form-control','id':'id_topic'}),
    )
        
class MatchingForm(ModelForm):
    class Meta:
        model = MatchingTeacher
        fields = '__all__'
        exclude = ['user']
