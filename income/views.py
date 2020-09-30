from time import strftime

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Income, Category
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required(login_url='/accounts/login')
def index(request):
    all_income = Income.objects.all();
    pagination_object = Paginator(all_income, 4)
    current_page_num = request.GET.get('page')
    all_income_pagination = Paginator.get_page(pagination_object, current_page_num)
    income = {
        'income': all_income,
        'page_obj': all_income_pagination
    }
    return render(request, 'income/index.html', income)


class AddIncomeView(LoginRequiredMixin, View):
    # Redirect to login
    login_url = '/accounts/login'

    categories = Category.objects.all();
    category_context = {
        'categories': categories
    }

    def get(self, request):
        return render(request, 'income/add_income.html', self.category_context)

    def post(self, request):
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        category = request.POST.get('category')
        date = request.POST.get('income_date')

        if amount is None or description is None or category is None or date is None:
            messages.add_message(request, messages.ERROR, 'Please enter all the details')
            return render(request, 'income/add_income.html', self.category_context)
        else:
            owner = request.user
            new_income_entry = Income.objects.create(amount=amount, description=description, category=category,
                                                     owner=owner, date=date)
            new_income_entry.save()
            messages.add_message(request, messages.SUCCESS, 'Income Successfully added')
            return redirect('income_homepage')


class EditIncomeView(LoginRequiredMixin, View):
    # Redirect to login
    login_url = '/accounts/login'

    def get(self, request):
        income_for_id = request.GET.get('income_id')
        income_to_edit = Income.objects.filter(pk=income_for_id)
        income_to_edit = {
            'amount': income_to_edit.values()[0]['amount'],
            'description': income_to_edit.values()[0]['description'],
            'category': income_to_edit.values()[0]['category'],
            'date': income_to_edit.values()[0]['date'],
            'id': income_for_id
        }
        categories = Category.objects.all();
        context = {
            'categories': categories,
            'income_to_edit': income_to_edit,
        }
        return render(request, 'income/edit_income.html', {'context': context})

    def post(self, request):
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        category = request.POST.get('category')
        date = request.POST.get('income_date')
        income_id = request.POST.get('income_id')

        if amount is None or description is None or category is None or date is None:
            messages.add_message(request, messages.ERROR, 'Please enter all the details')
            return redirect(request, 'expenses/edit_income.html')
        else:
            income_to_update = Income.objects.get(id=income_id);
            income_to_update.amount = amount
            income_to_update.description = description
            income_to_update.category = category
            income_to_update.date = date
            income_to_update.save()
            messages.add_message(request, messages.SUCCESS, 'Income Updated Successfully')
            return redirect('income_homepage')
