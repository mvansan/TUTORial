from django.forms import ModelForm
from .models import Question
from django import forms
from .models import Question, MatchingTeacher
from .models import UserInfo

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['topic','subtopic','title','body']


# class AddressForm(forms.Form):
#     subtopic = forms.ChoiceField(
#         choices = get_topic(),
#         required = False,
#         label='トピック',
#         widget=forms.Select(attrs={'class':'form-control','id':'id_topic'}),
#     )
        
class MatchingForm(ModelForm):
    class Meta:
        model = MatchingTeacher
        fields = '__all__'
        exclude = ['user']



class UserInfoForm(forms.ModelForm):
    profile_picture = forms.ImageField(label="プロフィール写真")
    name = forms.CharField(label="氏名")
    #age = forms.CharField(label="年齢")
    job = forms.CharField(label="職業")
    phone_number = forms.CharField(label="電話番号")
    email = forms.CharField(label="メールアドレス")
    about_me = forms.CharField(label="自分について", widget=forms.Textarea)
    meeting_app = forms.CharField(label="使用可能なオンラインミーティングapp")
    class Meta:
        model = UserInfo
        fields = ['profile_picture','name','age','job','phone_number','email','about_me','meeting_app']
        labels = {'age':"年齢"}


