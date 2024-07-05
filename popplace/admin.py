from django.contrib import admin

from .models import PopupStore,Location, Category, Reservation

admin.site.register(PopupStore)
admin.site.register(Location)
admin.site.register(Category)
admin.site.register(Reservation)