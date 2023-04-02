from django.shortcuts import render

# Create your views here.
def home_view(request):
    return render(request, 'menu/home.html')

def other_view(request):
    return render(request, 'menu/other.html')