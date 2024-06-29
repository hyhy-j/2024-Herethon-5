from django.shortcuts import render

# Create your views here.
def splash(request):
    return render(request, 'frontend/splash.html')

def main(request):
    return render(request, 'frontend/main.html')

def search(request):
    return render(request, 'frontend/search.html')

def map(request):
    return render(request, 'frontend/map.html')

def magazine(request):
    return render(request, 'frontend/magazine.html')

def mypage(request):
    return render(request, 'frontend/mypage.html')

def login(request):
    return render(request, 'frontend/login.html')

def signup(request):
    return render(request, 'frontend/signup.html')

def signdone(request):
    return render(request, 'frontend/signdone.html')

def popupstore(request):
    return render(request, 'frontend/popupstore.html')

def popupreserv(request):
    return render(request, 'frontend/popupreserv.html')