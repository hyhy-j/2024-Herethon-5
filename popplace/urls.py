from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='popplace'

urlpatterns = [
  path('', views.splash, name='splash'),
  path('main/', views.main, name='main'),
  path('search/', views.search, name='search'),
  path('map/', views.map, name='map'),
  path('category/', views.category, name='category'),
  # path('category/<str:category>/', views.category, name='category'),
  path('magazine/', views.magazine, name='magazine'),
  path('popupstore/', views.popupstore, name='popupstores'),
  path('popupstore/<int:popup_id>/', views.popupstore, name='popupstore'),
  path('popupstore/<int:popup_id>/reservation', views.popupreserv, name='popupreserv'),
  path('popupstore/<int:popup_id>/reserved',views.popupreserved, name='popupreserved'),
  path('popupstore/<int:popup_id>/review', views.popupreview, name='popupreview'),
  path('save_favorite/<int:popup_id>/', views.save_favorite, name='save_favorite'),
  
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)