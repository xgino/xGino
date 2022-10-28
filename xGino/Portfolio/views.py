from django.shortcuts import render
from django.http import HttpResponse

def portfolio_home(request):
    page = 'portfolio-home.html'
    context = {
        
    }

    return render(request, page, context)

