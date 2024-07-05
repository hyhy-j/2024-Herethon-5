from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from .models import PopupStore, Review, Location, Category,Reservation,Favorite
from .forms import ReviewForm, ReservationForm
from decimal import Decimal


# Create your views here.
def splash(request):
    return render(request, 'frontend/splash.html')

def main(request):
    popup = PopupStore.objects.all()
    context = {
        'popups': popup,
    }

    return render(request, 'frontend/main.html', context)


def search(request):
    categories = Category.objects.all()
    locations = Location.objects.all()
    
    query = request.GET.get('query', '')
    selected_category = request.GET.get('category', '')
    selected_location = request.GET.get('location', '')
    selected_date = request.GET.get('date', '')
    
    results = PopupStore.objects.all()
    
    if query:
        results = results.filter(name__icontains=query)
    
    if selected_category:
        results = results.filter(category__id=selected_category)
    
    if selected_location:
        results = results.filter(location__id=selected_location)
    
    if selected_date:
        results = results.filter(start_date__lte=selected_date, end_date__gte=selected_date)

    context = {
        'categories': categories,
        'locations': locations,
        'results': results,
        'query': query,
        'selected_category': selected_category,
        'selected_location': selected_location,
        'selected_date': selected_date,
    }
    return render(request, 'frontend/search.html', context)

def map(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', '')
    location_id = request.GET.get('location', '')
    date = request.GET.get('date', '')

    stores = PopupStore.objects.all()
    categories = Category.objects.all()
    locations = Location.objects.all()

    if query:
        stores = stores.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if category_id:
        stores = stores.filter(category__id=category_id)

    if location_id:
        stores = stores.filter(location__id=location_id)

    if date:
        stores = stores.filter(start_date__lte=date, end_date__gte=date)

    # 카테고리와 위치 이름을 포함하도록 수정
    store_list = []
    for store in stores:
        store_list.append({
            'id': store.id,
            'name': store.name,
            'address': store.address,
            'latitude': store.latitude,
            'longitude': store.longitude,
            'image': store.image,
            'category_name': store.category.name if store.category else '',
            'location_name': store.location.name if store.location else '',
            'start_date': store.start_date,
            'end_date': store.end_date
        })

    context = {
        'stores': store_list,
        'categories': categories,
        'locations': locations,
        'query': query,
        'selected_category': category_id,
        'selected_location': location_id,
        'selected_date': date,
    }
    return render(request, 'frontend/map.html', context)


def magazine(request):
    return render(request, 'frontend/magazine.html')


# def popupstore_list(request):
#     popups = PopupStore.objects.all()
#     context = {
#         'popups': popups,
#     }
#     return render(request, 'frontend/popupstore.html', context)
def popupstore(request, popup_id):
    popup = get_object_or_404(PopupStore, id=popup_id)
    reviews = popup.review_set.all()
    review_count = reviews.count()
    if reviews.exists():
        total_rate = sum(review.rate for review in reviews)
        average_rating = total_rate / Decimal(reviews.count())
    else:
        average_rating = Decimal('0.0')

    context = {
        'popup': popup,
        'popup_id': popup_id,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_count': review_count, 
    }
    return render(request, 'frontend/popupstore.html', {'popup': popup, 'popup_id': popup_id})

def add_favorite(request, popup_id):
    popup = get_object_or_404(PopupStore, id=popup_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, popup_store=popup)
    if created:
        message = '팝업스토어가 즐겨찾기에 추가되었습니다.'
    else:
        message = '팝업스토어가 이미 즐겨찾기에 있습니다.'
    return redirect('popplace:popupstore', popup_id=popup_id)

@login_required
def popupreserv(request, popup_id):
    popup = get_object_or_404(PopupStore, id=popup_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.popup_store = popup
            reservation.save()

            # 세션에 예약 정보 저장
            request.session['reservation_id'] = reservation.id

            return redirect('popplace:popupreserved', popup_id=popup_id) 
    else:
        form = ReservationForm()

    context = {
        'popup': popup,
        'form': form,
    }
    return render(request, 'frontend/popupreserv.html', context)


def popupreserved(request, popup_id):
    popup = get_object_or_404(PopupStore, id=popup_id)
    reservation_id = request.session.get('reservation_id')

    if reservation_id:
        reservation = get_object_or_404(Reservation, id=reservation_id)
    else:
        reservation = None

    popupl = PopupStore.objects.all()

    context = {
        'popup': popup,
        'reservation': reservation,
        'popuplist': popupl,
    }
    return render(request, 'frontend/popupreserved.html', {'popup': popup, 'popup_id': popup_id})

def popupreview(request, popup_id):

    popup = get_object_or_404(PopupStore, id=popup_id)
    reviews = Review.objects.filter(popup_store=popup)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.popup_store = popup
            review.save()
            return redirect('popplace:popupstore', popup_id=popup_id)
    else:
        form = ReviewForm()

    context = {
        'popup': popup,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'frontend/popupreview.html', context)

def category(request):
    category = request.GET.get('category')  # URL에서 카테고리 파라미터 받아오기
    popup_stores = PopupStore.objects.all()

    if category:
        popup_stores = popup_stores.filter(category=category)

    context = {
        'popup_stores': popup_stores,
        'selected_category': category,  # 선택된 카테고리를 템플릿에 전달
    }
    return render(request, 'frontend/category.html', context)

@login_required
def save_favorite(request, popup_id):
    if request.method == 'POST':
        popup = get_object_or_404(PopupStore, id=popup_id)
        user = request.user
        favorite, created = Favorite.objects.get_or_create(user=user, popup_store=popup)
        if created:
            messages.success(request, '팝업스토어가 즐겨찾기에 추가되었습니다.')
        else:
            messages.info(request, '팝업스토어가 이미 즐겨찾기에 있습니다.')
        return redirect('popplace:popupstore', popup_id=popup_id)
    messages.error(request, '잘못된 요청입니다.')
    return redirect('popplace:popupstore', popup_id=popup_id)