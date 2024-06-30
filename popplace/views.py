from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PopupStore, Review
from .forms import ReviewForm, SearchForm

# Create your views here.
def splash(request):
    return render(request, 'frontend/splash.html')

def main(request):
    return render(request, 'frontend/main.html')

def search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results=PopupStore.objects.filter(name__icontains=query)
        else:
            results =PopupStore.objects.none()
    else:
        form = SearchForm()
        results = PopupStore.objects.none()
    
    context={
        'form':form,
        'results':results,
    }
    return render(request, 'frontend/search.html',context)

def map(request):
    popup_stores = PopupStore.objects.all()
    return render(request, 'frontend/map.html', {'popup_stores': popup_stores})

# def magazine(request, magazine_id):
#     magazine= get_object_or_404(PopupStore,pk=magazine_id)
#     return render(request, 'frontend/magazine.html',{'magazine':magazine})

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

def popupstore(request, popup_id):
    popup = get_object_or_404(PopupStore, id = popup_id)
    reviews = popup.reviews.all()
    review_form = ReviewForm()
    context= {
        'popup':popup,
        'reviews':reviews,
        'review_form':review_form,
    }
    return render(request, 'frontend/popupstore.html',context)

@login_required
def popupreserv(request):
    return render(request, 'frontend/popupreserv.html')

def popupreview(request):
    reviews = Review.objects.all()
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('popupreview')
    else:
        form = ReviewForm()
    return render(request, 'frontend/popupreview.html', {'reviews':reviews, 'forms':forms})
