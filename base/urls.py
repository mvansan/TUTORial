from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('', views.home, name="home"),
    path('question/', views.questionList, name="questionList"),
    path('question/<str:pk>/', views.question, name="question"),
    path('create-question/', views.createQuestion, name="create-question"),
    path('update-question/<str:pk>', views.updateQuestion, name="update-question"),
    path('delete-question/<str:pk>', views.deleteQuestion, name="delete-question"),
    path('form/',views.CreateReview.as_view(),name="form"),
    path('submit_review/', views.submit_review, name='submit_review'),
    path('user-info/', views.ItemCreateView.as_view(), name="user_info"),
    path('matching/', views.MatchingListView.as_view(), name="matching"),
    path('matching/result/', views.MatchingResultView.as_view(), name="matching-result"),
    path('match/',views.match,name="match"),
    path('assessmentform/',views.submit_review,name="assessmentform"), path('submit_review/', views.submit_review, name='submit_review'),
    path('teacher-profile/<int:pk>/', views.UserDetail.as_view(), name="teacher-profile"),
    path('complete/', views.complete, name="complete"),
]