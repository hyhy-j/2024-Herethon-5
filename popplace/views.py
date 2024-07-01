from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
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
            query = form.cleaned_data.get('query')  
            results = PopupStore.objects.filter(name__icontains=query)
        else:
            results = PopupStore.objects.none()
    else:
        form = SearchForm()
        results = PopupStore.objects.none()
    
    context = {
        'form': form,
        'results': results,
    }
    return render(request, 'frontend/search.html', context)

def map(request):
    query = request.GET.get('query', '')
    popup_stores = PopupStore.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
    data = [
        {
            'id': popup_store.id,
            'name': popup_store.name,
            'latitude': popup_store.latitude,
            'longitude': popup_store.longitude,
        }
        for popup_store in popup_stores
    ]
    return JsonResponse(data, safe=False)

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

# def popupstore_list(request):
#     popups = PopupStore.objects.all()
#     context = {
#         'popups': popups,
#     }
#     return render(request, 'frontend/popupstore.html', context)

def popupstore(request, popup_id):
    popup = get_object_or_404(PopupStore, id = popup_id)
    reviews = popup.review_set.all()
    context= {
        'popup':popup,
        'reviews':reviews,
    }
    return render(request, 'frontend/popupstore.html',context)

# @login_required
def popupreserv(request,popup_id):
    popup = get_object_or_404(PopupStore, id=popup_id)
    if request.method=='POST':
        return redirect('popplace:popupreserved', popup_id=popup_id)
    context={'popup':popup,}
    return render(request, 'frontend/popupreserv.html', context)

def popupreserved(request,popup_id):
    popup = get_object_or_404(PopupStore, id=popup_id)
    context = {'popup': popup,}
    return render(request, 'frontend/popupreserved.html', context)

def popupreview(request, popup_id):
    popup = get_object_or_404(PopupStore, id=popup_id)
    reviews = Review.objects.filter(popup_store=popup)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.popup_store = popup
            review.user = request.user
            review.save()
            return redirect('popupstore', popup_id=popup_id)
    else:
        form = ReviewForm()

    context = {
        'popup': popup,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'frontend/popupreview.html', context)

