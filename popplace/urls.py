from django.urls import path
from . import views

app_name='popplace'

urlpatterns = [
  path('', views.splash, name='splash'),
  path('main/', views.main, name='main'),
  path('search/', views.search, name='search'),
  path('map/', views.map, name='map'),
  path('magazine/', views.magazine, name='magazine'),
  path('mypage/', views.mypage, name='mypage'),
  path('login/', views.login, name='login'),
  path('signup/', views.signup, name='signup'),
  path('signup/done', views.signdone, name='signdone'),
  path('popupstore/', views.popupstore, name='popupstore'),
  path('popupstore/reservation', views.popupreserv, name='popupreserv'),
]