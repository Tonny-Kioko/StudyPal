from django.shortcuts import render

# Create your views here.

def Store(request):
    context = {}
    return render (request, 'index.html', context)