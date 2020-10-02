from django.urls import path
from .views import index, AddExpenseView,EditExpenseView, ExpenseCategorySummaryView

urlpatterns = [
    path('', index, name="expense_homepage"),
    path('add_expenses', AddExpenseView.as_view(), name="add_expense"),
    path('edit_expenses', EditExpenseView.as_view(), name="edit_expense"),
    path('expense_summary', ExpenseCategorySummaryView.as_view(), name="expense_summary")
]
