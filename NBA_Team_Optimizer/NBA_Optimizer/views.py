from django.shortcuts import render

def index(request):
    return render(request, 'NBA_Optimizer/index.html')