from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from calendar import monthrange
from datetime import timedelta, date
from django.contrib.auth.decorators import login_required


from django.db.models import (
    Sum,
    F,
    IntegerField,
    ExpressionWrapper
)

from . import services
from stores.models import Store
from stocks.models import Stock
from expenses.models import Expense
from sales.models import (
    Sale,
    SaleItem
)


########################################################################################################
################################################## #####################################################
# ---------->>----------->>------------> Tableau de bord <<---------<<--------------<<-----------------#
################################################## #####################################################
########################################################################################################

@login_required(login_url="accounts:login")
def dashboard(request, store_id=None):

    if request.user.role not in ["owner"]:
        return redirect("products:product_list")

    today = timezone.localdate()

    # =========================================================
    # MAGASIN
    # =========================================================

    stores = (
        Store.objects
        .for_company(request.user.company)
        .order_by("name")
    )

    selected_store = None

    if store_id:
        selected_store = get_object_or_404(
            Store.objects.for_company(request.user.company),
            id=store_id
        )

    # =========================================================
    # VENTES
    # =========================================================

    sales = (
        Sale.objects
        .for_company(request.user.company)
        .filter(status="validated")
    )

    stocks = Stock.objects.for_company(request.user.company)

    if selected_store:
        sales = sales.filter(store=selected_store)
        stocks = stocks.filter(store=selected_store)

    # =========================================================
    # STOCK
    # =========================================================

    total_stock = (
        stocks
        .aggregate(total=Sum("quantity"))["total"] or 0
    )

    total_purchase = (
        stocks
        .aggregate(
            total=Sum(
                ExpressionWrapper(
                    F("quantity") * F("product__purchase_price"),
                    output_field=IntegerField()
                )
            )
        )["total"] or 0
    )

    total_sale = (
        stocks
        .aggregate(
            total=Sum(
                ExpressionWrapper(
                    F("quantity") * F("product__sale_price"),
                    output_field=IntegerField()
                )
            )
        )["total"] or 0
    )

    total_profit = total_sale - total_purchase

    # =========================================================
    # ANNÉE SÉLECTIONNÉE
    # =========================================================

    try:
        selected_year = int(
            request.GET.get("year", today.year)
        )
    except (ValueError, TypeError):
        selected_year = today.year

    # =========================================================
    # MOIS SÉLECTIONNÉ
    # =========================================================

    try:
        selected_month = int(
            request.GET.get("month", today.month)
        )
    except (ValueError, TypeError):
        selected_month = today.month

    if selected_month < 1 or selected_month > 12:
        selected_month = today.month

    month_start = date(
        selected_year,
        selected_month,
        1
    )

    month_end = date(
        selected_year,
        selected_month,
        monthrange(
            selected_year,
            selected_month
        )[1]
    )

    # =========================================================
    # MOIS PRÉCÉDENT
    # =========================================================

    if selected_month == 1:

        previous_month = 12
        previous_month_year = selected_year - 1

    else:

        previous_month = selected_month - 1
        previous_month_year = selected_year

    previous_month_start = date(
        previous_month_year,
        previous_month,
        1
    )

    previous_month_end = date(
        previous_month_year,
        previous_month,
        monthrange(
            previous_month_year,
            previous_month
        )[1]
    )

    # =========================================================
    # CA DU MOIS SÉLECTIONNÉ
    # =========================================================

    ca_month = services.calculate_ca(
        sales,
        month_start,
        month_end
    )

    ca_last_month = services.calculate_ca(
        sales,
        previous_month_start,
        previous_month_end
    )

    # =========================================================
    # BÉNÉFICE DU MOIS
    # =========================================================

    profit_month = (
        SaleItem.objects
        .filter(
            sale__in=sales,
            sale__created_at__date__gte=month_start,
            sale__created_at__date__lte=month_end,
        )
        .aggregate(
            total=Sum(
                ExpressionWrapper(
                    (
                        F("unit_price")
                        - F("product__purchase_price")
                    ) * F("quantity"),
                    output_field=IntegerField()
                )
            )
        )["total"] or 0
    )

    profit_last_month = (
        SaleItem.objects
        .filter(
            sale__in=sales,
            sale__created_at__date__gte=previous_month_start,
            sale__created_at__date__lte=previous_month_end,
        )
        .aggregate(
            total=Sum(
                ExpressionWrapper(
                    (
                        F("unit_price")
                        - F("product__purchase_price")
                    ) * F("quantity"),
                    output_field=IntegerField()
                )
            )
        )["total"] or 0
    )

    # =========================================================
    # DÉPENSES DU MOIS
    # =========================================================

    expense_month = (
        Expense.objects
        .for_company(request.user.company)
        .filter(
            expense_date__gte=month_start,
            expense_date__lte=month_end,
            is_deleted=False,
        )
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    # =========================================================
    # BÉNÉFICE RÉEL
    # =========================================================

    real_profit = profit_month - expense_month

    # =========================================================
    # ANNÉE SÉLECTIONNÉE
    # =========================================================

    year_start = date(
        selected_year,
        1,
        1
    )

    year_end = date(
        selected_year,
        12,
        31
    )

    ca_year = services.calculate_ca(
        sales,
        year_start,
        year_end
    )

    # =========================================================
    # ANNÉE PRÉCÉDENTE
    # =========================================================

    ca_last_year = services.calculate_ca(
        sales,
        date(selected_year - 1, 1, 1),
        date(selected_year - 1, 12, 31)
    )

    # =========================================================
    # JOUR SÉLECTIONNÉ
    # =========================================================

    selected_day_str = request.GET.get(
        "day",
        today.strftime("%Y-%m-%d")
    )

    try:
        selected_day = date.fromisoformat(selected_day_str)

    except ValueError:
        selected_day = today

    ca_day = (
        sales
        .filter(created_at__date=selected_day)
        .aggregate(total=Sum("total"))["total"] or 0
    )

    # =========================================================
    # JOUR PRÉCÉDENT
    # =========================================================

    previous_day = selected_day - timedelta(days=1)

    ca_yesterday = (
        sales
        .filter(created_at__date=previous_day)
        .aggregate(total=Sum("total"))["total"] or 0
    )

    # =========================================================
    # SEMAINE SÉLECTIONNÉE
    # =========================================================

    selected_week_str = request.GET.get(
        "week_start",
        (
            today - timedelta(days=today.weekday())
        ).strftime("%Y-%m-%d")
    )

    try:
        selected_week_start = date.fromisoformat(
            selected_week_str
        )

    except ValueError:
        selected_week_start = (
            today - timedelta(days=today.weekday())
        )

    selected_week_end = (
        selected_week_start + timedelta(days=6)
    )

    ca_week = services.calculate_ca(
        sales,
        selected_week_start,
        selected_week_end
    )

    # =========================================================
    # SEMAINE PRÉCÉDENTE
    # =========================================================

    last_week_start = (
        selected_week_start - timedelta(days=7)
    )

    last_week_end = (
        selected_week_start - timedelta(days=1)
    )

    ca_last_week = services.calculate_ca(
        sales,
        last_week_start,
        last_week_end
    )

    # =========================================================
    # POURCENTAGES
    # =========================================================

    ca_day_change = services.percentage_change(
        ca_day,
        ca_yesterday
    )

    ca_week_change = services.percentage_change(
        ca_week,
        ca_last_week
    )

    ca_month_change = services.percentage_change(
        ca_month,
        ca_last_month
    )

    ca_year_change = services.percentage_change(
        ca_year,
        ca_last_year
    )

    profit_month_change = services.percentage_change(
        profit_month,
        profit_last_month
    )

    # =========================================================
    # TAUX
    # =========================================================

    taux_moyen = 0

    if ca_month:
        taux_moyen = (
            profit_month / ca_month
        ) * 100

    total_taux_moyen = 0

    if total_purchase:
        total_taux_moyen = (
            total_profit / total_purchase
        ) * 100

    # =========================================================
    # LISTE DES ANNÉES
    # =========================================================

    years = list(range(today.year, 2025, -1))

    # =========================================================
    # LISTE DES MOIS
    # =========================================================

    months = [
        (1, "Janvier"),
        (2, "Février"),
        (3, "Mars"),
        (4, "Avril"),
        (5, "Mai"),
        (6, "Juin"),
        (7, "Juillet"),
        (8, "Août"),
        (9, "Septembre"),
        (10, "Octobre"),
        (11, "Novembre"),
        (12, "Décembre"),
    ]

    # =========================================================
    # 30 DERNIERS JOURS
    # =========================================================

    days = []

    for i in range(30):

        day = today - timedelta(days=i)

        days.append({
            "date": day,
            "label": day.strftime("%d/%m/%Y")
        })

    # =========================================================
    # 4 DERNIÈRES SEMAINES
    # =========================================================

    current_week_start = (
        today - timedelta(days=today.weekday())
    )

    weeks = []

    for i in range(4):

        week_start = (
            current_week_start
            - timedelta(days=i * 7)
        )

        week_end = week_start + timedelta(days=6)

        weeks.append({
            "start": week_start,
            "end": week_end,
            "label": (
                f"{week_start.strftime('%d/%m')}"
                f" au "
                f"{week_end.strftime('%d/%m/%Y')}"
            )
        })

    # =========================================================
    # CONTEXT
    # =========================================================

    context = {

        "stores": stores,
        "selected_store": selected_store,

        # périodes
        "selected_year": selected_year,
        "selected_month": selected_month,
        "selected_day": selected_day,
        "selected_week_start": selected_week_start,

        "years": years,
        "months": months,
        "days": days,
        "weeks": weeks,

        # CA
        "ca_day": ca_day,
        "ca_week": ca_week,
        "ca_month": ca_month,
        "ca_year": ca_year,

        # variations
        "ca_day_change": ca_day_change,
        "ca_week_change": ca_week_change,
        "ca_month_change": ca_month_change,
        "ca_year_change": ca_year_change,

        # bénéfices
        "profit_month": profit_month,
        "profit_month_change": profit_month_change,

        # dépenses
        "expense_month": expense_month,

        # bénéfice réel
        "real_profit": real_profit,

        # stock
        "total_stock": total_stock,
        "total_purchase": total_purchase,
        "total_sale": total_sale,
        "total_profit": total_profit,

        "taux_moyen": round(taux_moyen, 1),
        "total_taux_moyen": round(
            total_taux_moyen,
            1
        ),
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )




########################################################################################################
################################################## #####################################################
# ---------->>----------->>------------> Rapport         <<---------<<--------------<<-----------------#
################################################## #####################################################
########################################################################################################
@login_required(login_url='accounts:login')
def rapport(request, store_id=None):
    if request.user.role not in ['owner']:
        return redirect("products:product_list")


    today = timezone.localdate()

    # debut de la semaine
    start_week = today - timedelta(days=today.weekday())



    stores = Store.objects.for_company(request.user.company).order_by('name')

    selected_store = None


    if store_id:
        selected_store = get_object_or_404(Store.objects.for_company(request.user.company), id=store_id)


    sales = Sale.objects.for_company(request.user.company).filter(status='validated')

    stocks = Stock.objects.for_company(request.user.company)

    # si un magasin est selectionné
    # on recupere uniquement les ventes
    # et achats de ce magasin
    if selected_store:
        sales = sales.filter(store=selected_store)

        stocks = stocks.filter(store=selected_store)


    total_stock = stocks.aggregate(total=Sum('quantity'))['total'] or 0


    # calcul = sum(quantité x prix d'achat)
    # ex: quantité de chaque ligne x son prix d'achat
    # puis on addition le tout
    # e.g : id=1, quantité=2, prix d'achat unitaire=10000
    # e.g : id=2, quantité=5, prix d'achat unitaire=2000
    #  la valeur du prix d'achat total du magasin = 2 x 10000 + 5 x 2000
    total_purchase = stocks.aggregate(total=Sum(
        ExpressionWrapper(F('quantity') * F('product__purchase_price'), output_field=IntegerField())
        ))['total'] or 0


    total_sale = stocks.aggregate(total=Sum(
        ExpressionWrapper(F('quantity') * F('product__sale_price'), output_field=IntegerField())
        ))['total'] or 0

    total_profit = total_sale - total_purchase


    # calcul du chiffres d'affaires
    # additionner le prix de toute les ventes du jour
    ca_day = sales.filter(created_at__date=today, status='validated').aggregate(total=Sum('total'))['total'] or 0

    ca_week = sales.filter(created_at__date__gte=start_week, status='validated').aggregate(total=Sum('total'))['total'] or 0

    ca_month = sales.filter(created_at__year=today.year, created_at__month=today.month, status='validated').aggregate(total=Sum('total'))['total'] or 0


    # JOUR PRÉCÉDENT
    yesterday = today - timedelta(days=1)
    ca_yesterday = sales.filter(created_at__date=yesterday, status='validated').aggregate(total=Sum('total'))['total'] or 0


    # SEMAINE PASSÉE
    start_last_week = start_week - timedelta(days=7)

    end_last_week = start_week - timedelta(days=1)

    ca_last_week = sales.filter(
            created_at__date__gte=start_last_week,
            created_at__date__lte=end_last_week,
            status='validated'
        ).aggregate(total=Sum('total'))['total'] or 0




    # MOIS PASSÉ
    if today.month == 1:
        last_month = 12
        last_month_year = today.year - 1
    else:
        last_month = today.month - 1
        last_month_year = today.year

    ca_last_month = sales.filter(
            created_at__year=last_month_year,
            created_at__month=last_month,
            status='validated'
        ).aggregate(total=Sum('total'))['total'] or 0




    # ANNÉE EN COURS
    ca_year = sales.filter(created_at__year=today.year, status='validated').aggregate(total=Sum('total'))['total'] or 0

    # ANNÉE PASSÉE
    ca_last_year = sales.filter(created_at__year=today.year - 1, status='validated').aggregate(total=Sum('total'))['total'] or 0



    # calcul du pourcentage de chiffres
    # d'affaires actuel comparer aux precedent
    # chiffres d'affaires.
    # ex: ce mois et le mois precedent

    ca_day_change = services.percentage_change(ca_day, ca_yesterday)

    ca_week_change = services.percentage_change(ca_week, ca_last_week)

    ca_month_change = services.percentage_change(ca_month, ca_last_month)

    ca_year_change = services.percentage_change(ca_year, ca_last_year)


    # PROFIT MOIS PASSÉ
    profit_last_month = SaleItem.objects.filter(
            sale__in=sales, 
            sale__created_at__year=last_month_year,
            sale__created_at__month=last_month,
        ).aggregate(total=Sum(ExpressionWrapper(
            (F('unit_price') - F('product__purchase_price')) *
            F('quantity'), output_field=IntegerField())))['total'] or 0



    profit_month = SaleItem.objects.filter(
        sale__in=sales,
        sale__created_at__year=today.year,
        sale__created_at__month=today.month).aggregate(total=Sum(ExpressionWrapper(
            (F('unit_price') - F('product__purchase_price')) *
            F('quantity'), output_field=IntegerField())
        ))['total'] or 0


    # Depense du mois
    expense_month = Expense.objects.for_company(request.user.company).filter(
        expense_date__year=today.year,
        expense_date__month=today.month,
        is_deleted=False
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    # benefice réel
    real_profit = profit_month - expense_month


    # pourcentage du profit ce mois
    # par rapport au mois precedent
    profit_month_change = services.percentage_change(profit_month, profit_last_month)


    taux_moyen = 0
    if ca_month:
        taux_moyen = (profit_month / ca_month) * 100

    total_taux_moyen = 0
    if total_purchase:
        total_taux_moyen = (total_profit / total_purchase) * 100


    context = {
        'ca_day_change' : ca_day_change,
        'ca_week_change' : ca_week_change,
        'ca_month_change' : ca_month_change,
        'ca_year_change' : ca_year_change,
        'profit_month_change' : profit_month_change,

        'stores': stores,
        'selected_store': selected_store,

        'ca_day': ca_day,
        'ca_week': ca_week,
        'ca_month': ca_month,
        'ca_year' : ca_year,

        'profit_month': profit_month,
        'expense_month' : expense_month,
        'real_profit' : real_profit,

        'total_stock': total_stock,
        'total_purchase': total_purchase,
        'total_sale': total_sale,
        'total_profit': total_profit,


        'taux_moyen': round(taux_moyen, 1),
        'total_taux_moyen': round(total_taux_moyen, 1),
    }

    return render(request, 'dashboard/rapport.html', context)