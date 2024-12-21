# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Hall, Movie, Session, Seat, isReservation

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    pass

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    pass
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    pass
@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    pass
@admin.register(isReservation)
class ReservationAdmin(admin.ModelAdmin):
    pass