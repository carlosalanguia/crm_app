from django.db.models import OuterRef, Subquery, Q
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import Customer, Interaction

def customer_list(request):
    newest_interaction = Interaction.objects.filter(
        customer=OuterRef('pk')
    ).order_by('-date')
    
    customers = Customer.objects.annotate(
        last_interaction_date=Subquery(newest_interaction.values('date')[:1]),
        last_interaction_type=Subquery(newest_interaction.values('interaction_type')[:1])
    )

    query = request.GET.get('q')
    if query:
        customers = customers.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) |
            Q(company__name__icontains=query)
        )

    birthday_filter = request.GET.get('birthday')
    if birthday_filter == 'week':
        today = timezone.now().date()
        dates = [today + timedelta(days=i) for i in range(8)]
        month_days = [(d.month, d.day) for d in dates]
        
        q_birthday = Q()
        for month, day in month_days:
            q_birthday |= Q(birthday__month=month, birthday__day=day)
        
        customers = customers.filter(q_birthday)

    sort_by = request.GET.get('sort', 'last_name')
    if sort_by == 'last_interaction':
        customers = customers.order_by('-last_interaction_date')
    elif sort_by == 'birthday':
        customers = customers.order_by('birthday')
    elif sort_by == 'company':
        customers = customers.order_by('company__name')
    else:
        customers = customers.order_by('last_name', 'first_name')

    return render(request, 'crm/customer_list.html', {'customers': customers})

