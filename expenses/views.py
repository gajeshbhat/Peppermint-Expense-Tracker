import csv
import xlwt

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Expense, Category
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponse


@login_required(login_url='/accounts/login')
def index(request):
    all_expenses = Expense.objects.filter(owner=request.user);
    pagination_object = Paginator(all_expenses, 4)
    current_page_num = request.GET.get('page')
    expense_pagination = Paginator.get_page(pagination_object, current_page_num)
    expenses = {
        'expenses': all_expenses,
        'page_obj': expense_pagination
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
            return redirect('expense_homepage')


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
            'date': expense_to_edit.values()[0]['date'],
            'id': expense_for_id
        }
        categories = Category.objects.all();
        context = {
            'categories': categories,
            'expense_to_edit': expense_to_edit,
        }
        return render(request, 'expenses/edit_expense.html', {'context': context})

    def post(self, request):
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        category = request.POST.get('category')
        date = request.POST.get('expense_date')
        expense_id = request.POST.get('expense_id')

        if amount is None or description is None or category is None or date is None:
            messages.add_message(request, messages.ERROR, 'Please enter all the details')
            return redirect(request, 'expenses/edit_income.html')
        else:
            expense_to_update = Expense.objects.get(id=expense_id);
            expense_to_update.amount = amount
            expense_to_update.description = description
            expense_to_update.category = category
            expense_to_update.date = date
            expense_to_update.save()
            messages.add_message(request, messages.SUCCESS, 'Expense Updated Successfully')
            return redirect('expense_homepage')


class ExpenseCategorySummaryView(View):
    def get(self, request):
        today_date = datetime.today()
        six_month_ago = today_date - timedelta(days=180);
        expenses_six_months = Expense.objects.filter(date__gte=six_month_ago, date__lte=today_date)
        expense_by_category = self.get_expense_by_category(expenses_six_months)
        print(type(expense_by_category))
        return JsonResponse(expense_by_category)

    def get_expense_by_category(self, expenses_six_months):
        all_category_expense_sum = {}
        for expense in expenses_six_months:
            if expense.category not in all_category_expense_sum:
                all_category_expense_sum[expense.category] = expense.amount
            else:
                all_category_expense_sum[expense.category] += expense.amount

        return all_category_expense_sum


def export_csv(request):
    csv_response = HttpResponse(content_type='text/csv')
    csv_response['Content-disposition'] = str('attachment; filename=peppermint_expenses' + str(datetime.now()) + '.csv')
    expense_writer = csv.writer(csv_response)
    expense_writer.writerow(['Amount', 'Description', 'Category', 'Date'])

    all_expense_objects = Expense.objects.filter(owner=request.user);

    for expense in all_expense_objects:
        expense_writer.writerow([expense.amount, expense.description, expense.category, expense.date])

    return csv_response


def export_excel(request):
    xls_response = HttpResponse(content_type='application/ms-excel')
    xls_response['Content-disposition'] = str('attachment; filename=peppermint_expenses' + str(datetime.now()) + '.xls')
    expense_workbook = xlwt.Workbook(encoding='utf-8')
    expense_worksheet = expense_workbook.add_sheet('Expense')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    expense_columns = ['Amount', 'Description', 'Category', 'Date']

    for col_num in range(len(expense_columns)):
        expense_worksheet.write(row_num, col_num, expense_columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    all_expense_objects = Expense.objects.filter(owner=request.user).values_list('amount', 'description', 'category',
                                                                                 'date');

    for row in all_expense_objects:
        row_num += 1

        for col_num in range(len(row)):
            expense_worksheet.write(row_num, col_num, str(row[col_num]), font_style)

    expense_workbook.save(xls_response)
    return xls_response


def export_pdf(request):
    pdf_response = HttpResponse(content_type='application/pdf')
    pdf_response['Content-disposition'] = str('attachment; filename=peppermint_expenses' + str(datetime.now()) + '.pdf')

    return pdf_response
