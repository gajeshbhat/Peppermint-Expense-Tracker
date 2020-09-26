from django.urls import path
from .views import index, AddExpenseView

urlpatterns = [
    path('', index, name="expense_homepage"),
    path('expenses', AddExpenseView.as_view(), name="add_expense")
]
