from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True)
    
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_NOT_SPECIFIED = 2
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female'), (GENDER_NOT_SPECIFIED, 'Not specified')]
    gender = models.IntegerField(choices=GENDER_CHOICES, default=GENDER_NOT_SPECIFIED)
    
    ROLE_CHOICES = (('teacher', '講師'),('student', '生徒'))
    role = MultiSelectField(max_length=200, choices=ROLE_CHOICES, default='student')
    avatar = models.ImageField(null=True, default="avatar.svg")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Subtopic(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class MatchingTeacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    salary = models.IntegerField(null=True)
    
    DOWChoices = ((1, '月'),
                (2, '火'),
                (3, '水'),
                (4, '木'),
                (5, '金'),
                (6, '土'),
                (7, '日'))
    time = MultiSelectField(max_length=200, choices=DOWChoices, null=True)
    def __str__(self):
        return self.user.username
    
class MatchingStudent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    salary_min = models.IntegerField(null=True)
    salary_max = models.IntegerField(null=True)
    DOW_CHOICES = ((1, '月'),
                (2, '火'),
                (3, '水'),
                (4, '木'),
                (5, '金'),
                (6, '土'),
                (7, '日'))
    time = MultiSelectField(max_length=200, choices=DOW_CHOICES, null=True)
    def __str__(self):
        return self.user.username
    
class Point(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    point = models.IntegerField()
    
    def __str__(self):
        return self.point
    
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated','-created']
    
    def __str__(self):
        return self.title
    
class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.body[0:50]
    

class Review(models.Model):
    user_id = models.CharField(max_length=10)
    teacher_id = models.CharField(max_length=10)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Review by {self.user_id}"
    

class UserInfo(models.Model):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    job = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    about_me = models.TextField()
    meeting_app = models.CharField(max_length=100)
