from django.urls import path
from .views import index, AddIncomeView,EditIncomeView

urlpatterns = [
    path('', index, name="income_homepage"),
    path('add_income', AddIncomeView.as_view(), name="add_income"),
    path('edit_income', EditIncomeView.as_view(), name="edit_income")
]
