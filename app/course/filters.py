from django_filters import FilterSet
from . import models


class PriceFilter(FilterSet):
    class Meta:
        model = models.Course
        fields = {
            'price': ['gte', 'lte']
        }
