from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Topic, Subtopic, Matching, Point, Question, Answer
from .forms import QuestionForm
from django.http.response import JsonResponse
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

def my_view(request):
    # トピックとサブトピックのデータを取得
    topics = ["プログラミング", "アート"]
    programming_subcategories = ["ウェブ開発", "モバイルアプリ開発"]
    art_subcategories = ["絵画", "彫刻"]
    
    # サブトピックをトピックに関連付けて辞書に格納
    topic_subcategories = {
        "プログラミング": programming_subcategories,
        "アート": art_subcategories,
    }

    return render(request, 'doroppudowan.html', {
        'topics': topics,
        'topic_subcategories': topic_subcategories,
    })

def submit_review(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        teacher_id = request.POST['teacher_id']
        rating = request.POST['rating']
        comment = request.POST['comment']

        review = Review(user_id=user_id, teacher_id=teacher_id, rating=rating, comment=comment)
        review.save()

    return render(request, 'assessmentform.html')
