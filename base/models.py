from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True)
    
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_NOT_SPECIFIED = 2
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female'), (GENDER_NOT_SPECIFIED, 'Not specified')]
    gender = models.IntegerField(choices=GENDER_CHOICES, default=GENDER_NOT_SPECIFIED)
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
    
class Matching(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    class DOW(models.IntegerChoices):
        月 = 1
        火 = 2
        水 = 3
        木 = 4
        金 = 5
        土 = 6
        日 = 7
        
    time = models.IntegerField(choices=DOW.choices)   
    def __str__(self):
        return self
    
class Point(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    point = models.IntegerField()
    
    def __str__(self):
        return self.point
    
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    body = models.TextField()
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.body[0:50]
    
class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.body[0:50]