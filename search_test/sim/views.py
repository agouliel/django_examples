from django.shortcuts import render
from .models import Person


def search_view(request):
    all_people = Person.objects.all()
    context = {'count': all_people.count()}
    return render(request, 'search.html', context)


def search_results_view(request):
    if request.method == 'POST':
        query = request.POST.get('search', '')
        print(f'{query = }')

        all_people = Person.objects.all()
        if query:
            people = all_people.filter(name__icontains=query)
        else:
            people = []

        context = {'people': people, 'count': all_people.count()}
        return render(request, 'search_results.html', context)