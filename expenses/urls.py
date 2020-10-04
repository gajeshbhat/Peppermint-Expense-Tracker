from django.urls import path
from .views import index, AddExpenseView,EditExpenseView, ExpenseCategorySummaryView, export_csv, export_excel, export_pdf

urlpatterns = [
    path('', index, name="expense_homepage"),
    path('add_expenses', AddExpenseView.as_view(), name="add_expense"),
    path('edit_expenses', EditExpenseView.as_view(), name="edit_expense"),
    path('expense_summary', ExpenseCategorySummaryView.as_view(), name="expense_summary"),
    path('export_csv', export_csv, name="export_csv"),
    path('export_xls', export_excel, name="export_xls"),
    path('export_pdf', export_pdf, name="export_pdf")
]
