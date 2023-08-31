import django_filters
from django import forms
from .models import Matching

class MatchingFilter(django_filters.FilterSet):
    salary = django_filters.RangeFilter()
    time = django_filters.MultipleChoiceFilter(
        choices=Matching.DOWChoices,
        widget=forms.CheckboxSelectMultiple(),
        lookup_expr='icontains',
        )
    
    class Meta:
        model = Matching
        fields = {
            'topic': ['exact'],
        }
        
    