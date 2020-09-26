from django.shortcuts import render
from .models import Expense, Category
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required(login_url='/accounts/login')
def index(request):
    return render(request, 'expenses/index.html')


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
