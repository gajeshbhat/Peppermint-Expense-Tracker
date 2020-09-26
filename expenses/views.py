from time import strftime

from django.shortcuts import render
from .models import Expense, Category
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required(login_url='/accounts/login')
def index(request):
    all_expenses = Expense.objects.all();
    expenses = {
        'expenses': all_expenses
    }
    return render(request, 'expenses/index.html', expenses)


class AddExpenseView(LoginRequiredMixin, View):
    # Redirect to login
    login_url = '/accounts/login'

    categories = Category.objects.all();
    category_context = {
        'categories': categories
    }

    def get(self, request):
        return render(request, 'expenses/add_expense.html', self.category_context)

    def post(self, request):
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        category = request.POST.get('category')
        date = request.POST.get('expense_date')

        if amount is None or description is None or category is None or date is None:
            messages.add_message(request, messages.ERROR, 'Please enter all the details')
            return render(request, 'expenses/add_expense.html', self.category_context)
        else:
            owner = request.user
            new_expense_entry = Expense.objects.create(amount=amount, description=description, category=category,
                                                       owner=owner, date=date)
            new_expense_entry.save()
            messages.add_message(request, messages.SUCCESS, 'Expense Successfully added')
            return render(request, 'expenses/index.html')


class EditExpenseView(LoginRequiredMixin, View):
    # Redirect to login
    login_url = '/accounts/login'

    def get(self, request):
        expense_for_id = request.GET.get('expense_id')
        expense_to_edit = Expense.objects.filter(pk=expense_for_id)
        expense_to_edit = {
            'amount': expense_to_edit.values()[0]['amount'],
            'description': expense_to_edit.values()[0]['description'],
            'category': expense_to_edit.values()[0]['category'],
            'date': expense_to_edit.values()[0]['date']
        }
        categories = Category.objects.all();
        context = {
            'categories': categories,
            'expense_to_edit': expense_to_edit,
        }
        return render(request, 'expenses/edit_expense.html', {'context': context})
