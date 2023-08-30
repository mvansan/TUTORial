from itertools import count
from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from .models import User, Topic, Subtopic, MatchingTeacher, MatchingStudent, Point, Question, Answer
from .forms import QuestionForm, MatchingForm
from .filters import MatchingFilter
from .models import Review
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def home(request):
    topics = Topic.objects.all()
    questions = Question.objects.all()
    context = {'questions':questions}
    return render(request, 'base/home.html', context)

def questionList(request):
    topics = Topic.objects.all()
    questions = Question.objects.all()
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
    return render(request, 'base/user_info.html')

def student_profile_view(request):
    return render(request, 'base/student-profile.html')

def teacher_profile_view(request):
    return render(request, 'base/teacher-profile.html')

def matching(request):
    matching_filter = MatchingFilter(request.GET, queryset=MatchingTeacher.objects.all())
    form = matching_filter.form
    matchings = matching_filter.qs
    context = {'form':form, 'matchings':matchings}
    return render(request, 'base/matching_result.html', context)

class MatchingListView(ListView):
    queryset = MatchingTeacher.objects.all()
    template_name = 'base/matching_result.html'
    context_object_name = 'matchings'
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = MatchingFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.filterset.form
        return context

def review(request):
    books = request.POST.get("book")
    teacherID = request.POST.get("teacherID")
    print(books)
    print(teacherID)
    context = {}
    return render(request, 'base/form.html',context)

"""def review(request):
    if request.mothod == 'POST':
        form = (request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            review.objects.create(text=text)
            return redirect('top-page')
        else:
            form = Review()
            return render(request,'base/form.html',{form:form})"""

def match(request):
    return render(request, 'base/match.html')

