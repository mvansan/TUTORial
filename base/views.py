from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Topic, Subtopic, Matching, Point, Question, Answer
from .forms import QuestionForm

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

def user_info(request):
    return render(request, 'base/user_info.html')


def student_profile_view(request):
    return render(request, 'base/student-profile.html')

def teacher_profile_view(request):
    return render(request, 'base/teacher-profile.html')

def submit_profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        introduction = request.POST.get('introduction')

        # ここで受け取ったデータをデータベースに保存するか、セッションに保持するなどの処理が行われる想定

        # student-profile.html にデータを渡して表示する
        return render(request, 'student-profile.html', {'name': name, 'introduction': introduction})
    
    return HttpResponseRedirect('/')