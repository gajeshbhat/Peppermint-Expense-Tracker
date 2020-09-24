from django.urls import path
from .views import index, add_expense

urlpatterns = [
    path('', index, name="expense_homepage"),
    path('expenses',add_expense,name="add_expense")
]