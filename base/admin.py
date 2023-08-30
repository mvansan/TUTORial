from django.contrib import admin

from .models import User, Topic, Matching, Question, Answer, Review, UserInfo

admin.site.register(User)
admin.site.register(Topic)
# admin.site.register(Matching, MatchingAdmin)
admin.site.register(Question)
admin.site.register(Answer)
# admin.site.register(Point)
admin.site.register(UserInfo)
admin.site.register(Review)
