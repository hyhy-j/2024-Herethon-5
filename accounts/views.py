from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate

from popplace.models import Reservation
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile, Stamp


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/accounts/signdone')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('/accounts/login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/accounts/login')

def signdone(request):
    return render(request, 'accounts/signdone.html')
def home(request):
    return render(request, 'accounts/home.html')

@login_required
def mypage(request):
    user = request.user

    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None

    reservations = Reservation.objects.filter(user=user)
    reservations_count = reservations.count()  # 예약 개수 계산
    stamps_count = Stamp.objects.filter(user=user).count()
    stamps = user.stamps.all()

    context = {
        'user': user,
        'profile': profile,
        'reservations': reservations,
        'reservations_count': reservations_count,  # 예약 개수 추가
        'stamps_count': stamps_count,
        'stamps': stamps,
        # 'popup': popup,
    }

    return render(request, 'accounts/mypage.html', context)

@login_required
def add_stamp(request):
    if request.method == 'POST':
        authentication_code = request.POST.get('authentication_code')

        # 예시로 설정된 인증 번호들 (실제 사용 시 데이터베이스 조회 등으로 처리해야 함)
        valid_authentication_codes = ['1234', '5678', '9999']

        if authentication_code in valid_authentication_codes:
            # 인증 번호가 일치할 경우 도장 추가
            user = request.user
            stamp = Stamp(user=user)
            stamp.save()

            # stamps_count 1 증가
            stamps_count = Stamp.objects.filter(user=user).count()

            messages.success(request, '도장이 추가되었습니다.')
            return redirect('/accounts/mypage')
        else:
            messages.error(request, '인증 번호가 올바르지 않습니다.')

    return render(request, 'accounts/add_stamp.html')

