from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from .models import User, Topic, Matching, Point, Question, Answer
from .forms import QuestionForm, MatchingForm
from .filters import MatchingFilter
from .models import Review

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

    return render(request, 'assessmentform.html')

def user_info(request):
    return render(request, 'base/user_info.html')

def student_profile_view(request):
    return render(request, 'base/student-profile.html')

def teacher_profile_view(request):
    return render(request, 'base/teacher-profile.html')

def matching(request):
    matching_filter = MatchingFilter(request.GET, queryset=Matching.objects.all())
    form = matching_filter.form
    matchings = matching_filter.qs
    context = {'form':form, 'matchings':matchings}
    return render(request, 'base/matching.html', context)

def matchingResult(request):
    matching_filter = MatchingFilter(request.GET, queryset=Matching.objects.all())
    matchings = matching_filter.qs
    points = Point.objects.all()
    context = {'matchings':matchings, 'points':points}
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
        return context