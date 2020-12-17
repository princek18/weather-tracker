from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("passView/<int:pk>", views.PassView, name="passView"),
    path("ticket/", views.ticketView, name='ticketView'),
    path("review/", views.reviewView, name="reviewView"),
    path("booked/", views.booked, name="booked"),
    path("history/", views.history, name="history"),
    path("bookhis/<int:pk>", views.bookhis, name="bookhis")
]
