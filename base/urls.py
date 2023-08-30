from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('question/', views.questionList, name="questionList"),
    path('question/<str:pk>/', views.question, name="question"),
    path('create-question/', views.createQuestion, name="create-question"),
    path('update-question/<str:pk>', views.updateQuestion, name="update-question"),
    path('delete-question/<str:pk>', views.deleteQuestion, name="delete-question"),
    path('assessmentform/',views.submit_review,name="assessmentform"),
     path('submit_review/', views.submit_review, name='submit_review'),
    path('user-info/', views.ItemCreateView.as_view(), name="user-info"),
    path('student-profile/<int:pk>/', views.UserDetail.as_view(), name="student-profile"),
    path('teacher-profile/', views.teacher_profile_view, name="teacher-profile"),
    path('matching/', views.MatchingListView.as_view(), name="matching"),
]