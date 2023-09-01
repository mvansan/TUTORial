import numpy as np
from itertools import count
from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import User, Topic, Matching, Question, Answer,  MatchingStatus
from .forms import QuestionForm, MatchingForm, UserInfoForm,TeacherReview
from .filters import MatchingFilter
from .models import Review
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password is not correct')
    context = {'page':page}
    return render(request, 'base/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    questions = Question.objects.all()
    context = {'questions':questions}
    return render(request, 'base/home.html', context)

def questionList(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    questions = Question.objects.filter(
        Q(topic__name__icontains=q) |
        Q(title__icontains=q)
        )
    topics = Topic.objects.all()
    question_count = questions.count()
    context = {'questions':questions, 'question_count':question_count, 'topics':topics}
    return render(request, 'base/question_list.html', context)

def question(request, pk):
    question = Question.objects.get(id=pk)
    answers = question.answer_set.all().order_by('-created')
    
    if request.method == 'POST':
        answer = Answer.objects.create(
            user=request.user,
            question =question,
            body=request.POST.get('body')
        )
        return redirect('question', pk=question.id)
    
    context = {'question': question, 'answers': answers}
    return render(request, 'base/question.html', context)

def createQuestion(request):
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('question', pk=question.id)
        
    context = {'form':form}
    return render(request, 'base/question_form.html', context)

def updateQuestion(request, pk):
    question = Question.objects.get(id=pk)
    form = QuestionForm(instance=question)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('question', pk=question.id)
        
    context = {'form':form}
    return render(request, 'base/question_form.html', context)


def deleteQuestion(request, pk):
    question = Question.objects.get(id=pk)
    if request.method == 'POST':
        question.delete()
        return redirect('questionList')
    return render(request, 'base/delete.html', {'obj':question})

def submit_review(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        teacher_id = request.POST['teacher_id']
        rating = request.POST['rating']
        comment = request.POST['comment']

        review = Review(user_id=user_id, teacher_id=teacher_id, rating=rating, comment=comment)
        review.save()

    return render(request, 'base/form.html')

def user_info(request):
    return render(request, 'base/user-info.html')

def student_profile_view(request):
    return render(request, 'base/student-profile.html')

def create_profile(request):
    if request.method == 'POST':
        form = UserInfoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile_created')  # プロフィールが作成された後のページへリダイレクト
    else:
        form = UserInfoForm()
    return render(request, 'create_profile.html', {'form': form})

def teacher_profile_view(request):
    return render(request, 'base/teacher-profile.html')

def createMatching(request):
    form = MatchingForm()
    if request.method == 'POST':
        form = MatchingForm(request.POST)
        if form.is_valid():
            matching = form.save(commit=False)
            matching.user = request.user
            matching.save()
            return redirect('home')
        
    context = {'form':form}
    return render(request, 'base/matching_form.html', context)

def myMatching(request):
    s_matched_matchings = MatchingStatus.objects.filter(user=request.user, status=2)
    s_pending_matchings = MatchingStatus.objects.filter(user=request.user, status=1)
    t_matched_matchings = MatchingStatus.objects.filter(teacher=request.user, status=2)
    t_pending_matchings = MatchingStatus.objects.filter(teacher=request.user, status=1)
    context = {
        's_matched_matchings':s_matched_matchings, 's_pending_matchings':s_pending_matchings,
        't_matched_matchings':t_matched_matchings, 't_pending_matchings':t_pending_matchings,
        }
    return render(request, 'base/my-matching.html', context)

def accept_matching_status(request, matching_id):
    matching_status = get_object_or_404(MatchingStatus, pk=matching_id)
    matching_status.status = 2  # Change status to 2 (matched)
    matching_status.save()
    return redirect('my-matching')

def decline_matching_status(request, matching_id):
    matching_status = get_object_or_404(MatchingStatus, pk=matching_id)
    matching_status.delete()  # Delete the matching status
    return redirect('my-matching')

def matching(request):
    matching_filter = MatchingFilter(request.GET, queryset=Matching.objects.all())
    form = matching_filter.form
    matchings = matching_filter.qs
    context = {'form':form, 'matchings':matchings,}
    return render(request, 'base/matching.html', context)

def matchingResult(request):
    matching_filter = MatchingFilter(request.GET, queryset=Matching.objects.all())
    matchings = matching_filter.qs

    context = {'matchings':matchings,}
    return render(request, 'base/matching-result.html', context)

def sent_matching_status(request, matching_id):
    matching = get_object_or_404(Matching, pk=matching_id)

    existing_status = MatchingStatus.objects.filter(user=request.user, teacher=matching.user).first()
    if existing_status:
        existing_status.status = 1
        existing_status.save()
    else:
        MatchingStatus.objects.create(user=request.user, teacher=matching.user, status=1)

    return redirect('my-matching')

def matchingSuccess(request,pk):
    matching_filter = MatchingFilter(request.GET, queryset=Matching.objects.all())
    matchings = matching_filter.qs

    context = {'matchings':matchings,}
    context = {}
    return render(request, 'base/matching-result.html', context)

class MatchingListView(ListView):
    queryset = Matching.objects.all()
    template_name = 'base/matching.html'
    context_object_name = 'matchings'
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = MatchingFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.filterset.form
        return context

class MatchingResultView(TemplateView):
    template_name = 'base/matching-result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        matching_filter = MatchingFilter(self.request.GET, queryset=Matching.objects.all())
        matchings = matching_filter.qs
        context['matchings'] = matchings

        selected_times = self.request.GET.getlist('time')  
        context['selected_times'] = selected_times

        for matching in matchings:
            matching_count = 0
            for selected_time in selected_times:
                if selected_time in matching.time:  
                    matching_count += 1
            matching.matching_count = matching_count
            
            scaled_point = matching.point / 700
            scaled_salary = matching.salary / 1500
            
            normalized_matching_count = (matching_count - 1) / 6
            normalized_point = -np.exp(-np.log(2) * scaled_point) + 1
            normalized_salary = np.exp(-np.log(2) * scaled_salary)
            
            weight_matching_count = 0.6
            weight_point = 0.3
            weight_salary = 0.1
            
            weighted_score = (weight_matching_count * normalized_matching_count) + (weight_point * normalized_point) + (weight_salary * normalized_salary)
            matching.priority = weighted_score
            matching.save()
        context['matchings'] = sorted(matchings, key=lambda instance: instance.priority, reverse=True)
        user = self.request.user
        context['user_matching_statuses'] = MatchingStatus.objects.filter(user=user)
        return context



# def review(request):
#     if request.method == 'POST':
#         score = request.FILES.get('books')  # ファイルアップロードの場合
#         name = request.POST.get('na')
#         age = request.POST.get('age')
#         job = request.POST.get('job')
#         phone_number = request.POST.get('phone_number')
#         email = request.POST.get('email')
#         about_me = request.POST.get('about_me')
#         meeting_app = request.POST.get('meeting_app')
        
#         # データベースに保存
#         user_info = UserInfoForm(
#             profile_picture=profile_picture,
#             name=name,
#             age=age,
#             job=job,
#             phone_number=phone_number,
#             email=email,
#             about_me=about_me,
#             meeting_app=meeting_app,
#         )
#         user_info.save()
        
#         return redirect('success_url')  # 登録成功後のURLにリダイレクト
    
#     return render(request, 'base/form.html')
   

    # # teacher = None
    # # rating = None
    # # comment = None
    # if request.method == 'POST':
    #     rating = request.POST.get("book")
    #     teacher = request.POST.get("teacher")
    #     comment = request.POST.get("comment")
    # # print(rating)
    # # print(teacher)

    # teach = Review(
    #     rating=rating,
    #     teacher=teacher,
    #     comment=comment,
    # )
    # teach.save()

    # return render(request, 'base/form.html')

    # books = request.POST.get("book")
    # teacherID = request.POST.get("teacherID")
    # print(books)
    # print(teacherID)
    # context = {}
    # return render(request, 'base/form.html',context)

# """def review(request):
#     if request.mothod == 'POST':
#         form = (request.POST)
#         if form.is_valid():
#             text = form.cleaned_data['text']
#             review.objects.create(text=text)
#             return redirect('top-page')
#         else:
#             form = Review()
#             return render(request,'base/form.html',{form:form})"""

def match(request):
    return render(request, 'base/match.html')


def user_info_view(request):
    if request.method == 'POST':
        profile_picture = request.FILES.get('profilePicture')  # ファイルアップロードの場合
        name = request.POST.get('name')
        age = request.POST.get('age')
        role = request.POST.get('role')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        about_me = request.POST.get('about_me')
        meeting_app = request.POST.get('meeting_app')
        
        # データベースに保存
        user_info = UserInfoForm(
            profile_picture=profile_picture,
            name=name,
            age=age,
            role=role,
            phone_number=phone_number,
            email=email,
            username = username,
            password = password,
            about_me=about_me,
            meeting_app=meeting_app,
        )
        user_info.save()
        
        return redirect('success_url')  # 登録成功後のURLにリダイレクト
    
    return render(request, 'base/user-info.html')


from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, DetailView
from django.urls import reverse_lazy
# Create your views here.
class ItemCreateView(CreateView):
    model = User
    form_class = UserInfoForm
    template_name = "base/user-info.html"
    success_url = reverse_lazy("complete")



class UserDetail(DetailView):
    model = User
    template_name = "base/teacher-profile.html"
class MatchingResultView(TemplateView):
    template_name = 'base/matching-result.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        matching_filter = MatchingFilter(self.request.GET, queryset=Matching.objects.all())
        matchings = matching_filter.qs
        context['matchings'] = matchings
        return context
    
class CreateReview(CreateView):
    model = Review
    form_class = TeacherReview
    template_name = "base/form.html"
    success_url = reverse_lazy("home")


# def createsubimit(request): #sutasubimit
#     form = QuestionForm()
#     if request.method == 'POST':
#         form = QuestionForm(request.POST)
#         if form.is_valid():
#             question = form.save(commit=False)
#             question.user = request.user
#             question.save()
#             return redirect('question', pk=question.id)
        
#     context = {'form':form}
#     return render(request, 'base/form.html', context)

    model = User
    template_name = "base/teacher-profile.html"

def complete(request):
    return render(request, 'base/complete.html')
