from django.contrib import admin

from .models import User, Topic, Matching, Question, Answer, Review, UserInfo

class MatchingAdmin(admin.ModelAdmin):
    list_display = ("user", "topic", "salary", "point", "time", "matching_count", "priority")

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Matching, MatchingAdmin)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserInfo)
admin.site.register(Review)
