from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("customers/", views.customers, name="customers"),
    path("history/", views.history, name="history"),
    path("transfer/", views.transfer, name="transfer"),
]