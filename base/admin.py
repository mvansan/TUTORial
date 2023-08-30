from django.contrib import admin

from .models import User, Topic, Matching, Question, Answer, Point, Review

class PointAdmin(admin.ModelAdmin):
    list_display = ("user","topic","point")

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Matching)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Point, PointAdmin)
admin.site.register(Review)
