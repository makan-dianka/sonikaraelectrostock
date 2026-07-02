from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from django.db.models import Sum

from sonikaraelectrostock.tools import generate_reference

from .forms import ExpenseForm
from .models import Expense
from django.http import HttpResponseForbidden
from django.utils import timezone




@login_required(login_url="accounts:login")
def expense_list(request):

    today = timezone.now().date()

    expenses = (
        Expense.objects
        .filter(is_deleted=False)
        .select_related(
            "store",
            "category",
            "created_by"
        )
        .order_by(
            "-expense_date",
            "-id"
        )
    )

    total_expense = (
        expenses.aggregate(total=Sum("amount"))["total"] or 0
    )

    expense_today = (
        expenses.filter(
            expense_date=today
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0
    )

    expense_month = (
        expenses.filter(
            expense_date__year=today.year,
            expense_date__month=today.month
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0
    )

    total_store = (
        expenses.values("store")
        .distinct()
        .count()
    )

    context = {
        "expenses": expenses,
        "total_expense": total_expense,
        "expense_today": expense_today,
        "expense_month": expense_month,
        "total_store": total_store,
    }

    return render(
        request,
        "expenses/list.html",
        context,
    )


@login_required(login_url="accounts:login")
def expense_create(request):

    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission de créer une dépense.")

    form = ExpenseForm(request.POST or None)

    if form.is_valid():

        expense = form.save(commit=False)

        expense.reference = generate_reference(
            "DEP",
            Expense
        )

        expense.created_by = request.user

        expense.save()

        messages.success(
            request,
            "La dépense a été enregistrée."
        )

        return redirect("expenses:list")

    return render(
        request,
        "expenses/form.html",
        {
            "form": form
        }
    )




@login_required(login_url='accounts:login')
def delete_expense(request, pk):
    if request.user.role not in ['owner']:
        return HttpResponseForbidden("Vous n'avez pas la permission de supprimer une dépense.")
    expense = get_object_or_404(Expense, id=pk)
    expense.is_deleted = True
    expense.save()
    return redirect('expenses:list')