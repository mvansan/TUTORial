import django_filters
from django import forms
from .models import MatchingTeacher

class MatchingFilter(django_filters.FilterSet):
    salary = django_filters.RangeFilter()
    time = django_filters.MultipleChoiceFilter(
        choices=MatchingTeacher.DOWChoices,
        widget=forms.CheckboxSelectMultiple(),
        lookup_expr='icontains',
        )
    
    class Meta:
        model = MatchingTeacher
        fields = {
            'topic': ['exact'],
        }
        
    