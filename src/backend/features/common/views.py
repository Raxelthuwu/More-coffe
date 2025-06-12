from django.shortcuts import render

def common(request):
    return render(request, 'common/index.html')  
