import numpy as np
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
    
    ROLE_CHOICES = [('teacher', '講師'),('student', '生徒')]
    role = models.CharField(max_length=200, unique=True, choices=ROLE_CHOICES, default='student')
    
    avatar = models.ImageField(null=True, default="avatar.svg")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Matching(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    salary = models.IntegerField(null=True)
    matching_count = models.IntegerField(default=0)
    
    DOWChoices = ((1, '月'),
                (2, '火'),
                (3, '水'),
                (4, '木'),
                (5, '金'),
                (6, '土'),
                (7, '日'))
    time = MultiSelectField(max_length=200, choices=DOWChoices, null=True)
    
    @property
    def point(self):
        answers = Answer.objects.filter(
            user=self.user, question__topic_id=self.topic_id
        )
        point = 0
        if(answers != None):
            for answer in answers:
                point += answer.like
            
        reviews = Review.objects.filter(
            teacher_id=self.user_id, topic_id=self.topic_id
        )
        if(reviews != None):
            for review in reviews:
                point += self._convert_rating_to_point(review.rating)
        return point
    
    def _convert_rating_to_point(self, rating):
        if rating == 1:
            return -100
        elif rating == 2:
            return -50
        elif rating == 3:
            return 0
        elif rating == 4:
            return 50
        elif rating == 5:
            return 100
        else:
            return 0
        
    @property
    def priority(self):
        scaled_point = self.point / 700
        scaled_salary = self.salary / 1500
        
        normalized_matching_count = (self.matching_count - 1) / 6
        normalized_point = -np.exp(-np.log(2) * scaled_point) + 1
        normalized_salary = np.exp(-np.log(2) * scaled_salary)

        
        weight_matching_count = 0.6
        weight_point = 0.3
        weight_salary = 0.1
        
        weighted_score = (weight_matching_count * normalized_matching_count) + (weight_point * normalized_point) - (weight_salary * normalized_salary)

        return weighted_score
    
    
    def __str__(self):
        return self.user.username
    
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
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
    like = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.body[0:50]
    

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_review')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_review')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField()
    comment = models.TextField()
def __str__(self):
        return f"Review by {self.user_id}"
    

class Contact(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'contacts'
class MatchingStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_status')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_status')

    
    
class UserInfo(models.Model):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    job = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    about_me = models.TextField()
    meeting_app = models.CharField(max_length=100)
