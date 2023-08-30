from django.contrib import admin

from .models import User, Topic, Subtopic, MatchingTeacher, MatchingStudent, Question, Answer, Point, UserInfo

class MatchingAdmin(admin.ModelAdmin):
    list_display = ("user","topic","salary","point","time")

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Matching, MatchingAdmin)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Point)
admin.site.register(UserInfo)
admin.site.register(Review)
