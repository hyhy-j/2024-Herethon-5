from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from .models import PopupStore, Review, Location, Category,Reservation,Favorite
from .forms import ReviewForm, SearchForm, ReservationForm
from decimal import Decimal

# Create your views here.
def splash(request):
    return render(request, 'frontend/splash.html')

def main(request):
    return render(request, 'frontend/main.html')

def search(request):
    popup = PopupStore.objects.all()

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
        'popup_stores': popup,
        'results': results,
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


def magazine(request, magazine_id):
    magazine= get_object_or_404(PopupStore,pk=magazine_id)
    return render(request, 'frontend/magazine.html',{'magazine':magazine})

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
        'reviews': reviews,
        'average_rating': average_rating,
        'review_count': review_count, 
    }
    return render(request, 'frontend/popupstore.html', context)

def add_favorite(request, popup_id):
    popup = get_object_or_404(PopupStore, id=popup_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, popup_store=popup)
    if created:
        message = '팝업스토어가 즐겨찾기에 추가되었습니다.'
    else:
        message = '팝업스토어가 이미 즐겨찾기에 있습니다.'
    return redirect('popplace:popupstore', popup_id=popup_id)

# @login_required
def popupreserv(request, popup_id):
    popup = get_object_or_404(PopupStore, id=popup_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
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

    context = {
        'popup': popup,
        'reservation': reservation,
    }
    return render(request, 'frontend/popupreserved.html', context)

def popupreview(request, popup_id):

    popup = get_object_or_404(PopupStore, id=popup_id)
    reviews = Review.objects.filter(popup_store=popup)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.popup_store = popup
            # review.user = request.user
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



# def category(request, category):
#     # 작은 카테고리에 따라 해당하는 팝업들을 가져와 JSON 형태로 반환
#     popups = PopupStore.objects.filter(category__iexact=category)  # 대소문자 구분 없이 필터링
#     data = list(popups.values('name', 'description'))  # 필요한 필드만 JSON으로 변환
    
#     return JsonResponse(data, safe=False)