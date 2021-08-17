""" Views for handling posting search functions """

# Django core imports
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q

# Third-party imports

# App imports
from jobs_backend.app.models import Posting


# View for generating a template for doing searches among postings
def SearchView(request):
    return render(request, 'main/search/search.html')

# View for showing search results (invoked on each keystroke in the search-form) 
def SearchQuery(request):

    # Get the searchterm from the form
    search = request.GET.get("search")

    # Get all postings available to search from
    queryset = Posting.objects.all()

    # Initiating list for storing search results
    payload = []

    if search:

        # Filter out postings that match query
        queryset = queryset.filter(Q(title__icontains=search) | Q(work_title__icontains=search))
        
        # Append each result to the list that should be returned
        for result in queryset:
            payload.append(result.title + " || " + result.work_title + " || " + "id: " + str(result.id))
    
    # Returning list with results along with status code
    return JsonResponse({'status': 200, 'data': payload})