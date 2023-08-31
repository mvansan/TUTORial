from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True)
    
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    age = models.PositiveIntegerField(default=0)
    job = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    about_me = models.TextField(null=True)
    meeting_app = models.CharField(max_length=100)
    
    class Role(models.IntegerChoices):
        Student = 1
        Teacher = 2
    
    role = models.IntegerField(choices=Role.choices, default='1')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Matching(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    salary = models.IntegerField(null=True)
    matching_count = models.IntegerField(default=0)
    priority = models.FloatField(default=0)
    
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
    status = models.IntegerField(null=True)
