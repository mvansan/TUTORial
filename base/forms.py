from django.forms import ModelForm
from .models import Question
from django import forms
from .models import Question,Review
from .models import Question, Matching
from .models import User

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['topic','title','body']


# class starForm(ModelForm):
#     class Meta:
#         model = Question
#         fields = ['topic','title','body']


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
        exclude = ['user','matching_count', 'priority']


"""class Review(ModelForm):
    class Meta:
        model = Review
        fields = ['comment']"""

        

class UserInfoForm(forms.ModelForm):
    profile_picture = forms.ImageField(label="プロフィール写真")
    name = forms.CharField(label="氏名")
    #age = forms.CharField(label="年齢")
    Role_Choices =(
    ("1", "Student"),
    ("2", "Teacher"),
    )
    role = forms.ChoiceField(label="職業",widget=forms.RadioSelect,choices=Role_Choices)
    phone_number = forms.CharField(label="電話番号")
    email = forms.CharField(label="メールアドレス")
    username = forms.CharField(label="ユーザー名")
    password = forms.CharField(label="パスワード", widget = forms.PasswordInput())
    about_me = forms.CharField(label="自分について", widget=forms.Textarea)
    meeting_app = forms.CharField(label="使用可能なオンラインミーティングapp")
    class Meta:
        model = User
        fields = ['profile_picture','name','age','role','phone_number','email','username','password','about_me','meeting_app']
        labels = {'age':"年齢"}

class TeacherReview(forms.ModelForm):
    teacherID = forms.CharField(label='teacherID')
    score = forms.IntegerField(label="score")
    text = forms.TimeField(label='評価')
    class Meta:
        model = Review
        fields = ['teacherID','score','text']
        
