from django.contrib import admin

from .models import User, Topic, Subtopic, Matching, Question, Answer

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Subtopic)
admin.site.register(Matching)
admin.site.register(Question)
admin.site.register(Answer)
