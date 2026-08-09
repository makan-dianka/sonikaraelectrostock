from django.db.models import Sum

def percentage_change(current, previous):
    if previous == 0:
        if current > 0:
            return 100
        return 0
    return round(((current - previous) / previous) * 100, 2)




def calculate_ca(queryset, start_date, end_date):
    return (
        queryset
        .filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date,
        )
        .aggregate(total=Sum("total"))["total"] or 0
    )