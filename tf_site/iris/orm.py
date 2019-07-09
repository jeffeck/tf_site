from django.db.models import Avg, Count, Max, Min, StdDev, Sum, Variance

"""
The purpose of this file is to provide Object Relational Mappings ORMs
that demonstrate the equivalence to SQL.
A generic 'model' should be passed in to each function.

"""

def counts_by_class(model):
    """
    Retrieves all objects from the model and provides a count for each classification
    """
    # SELECT classification 
    # , count() 
    # FROM iris 
    # GROUP BY classification 
    return model.objects.values('classification').annotate(Count('classification'))


def avg_by_class(model, field):
    """
    Retrieves all objects from the model and provides the average for each classification
    """
    # SELECT classification 
    # ,avg(), count(), max(), min(), stddev(), sum(), variance()
    # FROM iris 
    # GROUP BY classification 
    return model.objects.values('classification').annotate(
        avg=Avg(field), 
        count=Count(field), 
        max=Max(field), 
        min=Min(field), 
        stddev=StdDev(field), 
        sum=Sum(field), 
        variance=Variance(field),
    )

