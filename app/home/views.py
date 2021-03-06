from django.shortcuts import render

# Create your views here.


def comingsoon(request):
    return render(request, 'comingsoon.html')
