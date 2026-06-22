from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
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
from sales.models import (
    Sale,
    SaleItem
)


########################################################################################################
################################################## #####################################################
# ---------->>----------->>------------> Tableau de bord <<---------<<--------------<<-----------------#
################################################## #####################################################
########################################################################################################
@login_required(login_url='account:login')
def dashboard(request, store_id=None):

    today = timezone.now().date()

    # debut de la semaine
    start_week = today - timedelta(days=today.weekday())



    stores = Store.objects.all()

    selected_store = None


    if store_id:
        selected_store = get_object_or_404(Store, id=store_id)


    sales = Sale.objects.all()
    stocks = Stock.objects.all()

    # si un magasin est selectionné
    # on recupere uniquement les ventes
    # et achats de ce magasin
    if selected_store:
        sales = sales.filter(store=selected_store)
        stocks = stocks.filter(store=selected_store)



    if request.user.role != 'owner':
        sales = sales.filter(user=request.user)


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
    ca_day = sales.filter(created_at__date=today).aggregate(total=Sum('total'))['total'] or 0

    ca_week = sales.filter(created_at__date__gte=start_week).aggregate(total=Sum('total'))['total'] or 0

    ca_month = sales.filter(created_at__year=today.year, created_at__month=today.month).aggregate(total=Sum('total'))['total'] or 0


    # JOUR PRÉCÉDENT
    yesterday = today - timedelta(days=1)
    ca_yesterday = sales.filter(created_at__date=yesterday).aggregate(total=Sum('total'))['total'] or 0


    # SEMAINE PASSÉE
    start_last_week = start_week - timedelta(days=7)

    end_last_week = start_week - timedelta(days=1)

    ca_last_week = sales.filter(
            created_at__date__gte=start_last_week,
            created_at__date__lte=end_last_week
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
            created_at__month=last_month
        ).aggregate(total=Sum('total'))['total'] or 0




    # ANNÉE EN COURS
    ca_year = sales.filter(created_at__year=today.year).aggregate(total=Sum('total'))['total'] or 0

    # ANNÉE PASSÉE
    ca_last_year = sales.filter(created_at__year=today.year - 1).aggregate(total=Sum('total'))['total'] or 0



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
            sale__created_at__month=last_month
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

        'total_stock': total_stock,
        'total_purchase': total_purchase,
        'total_sale': total_sale,
        'total_profit': total_profit,


        'taux_moyen': round(taux_moyen, 1),
        'total_taux_moyen': round(total_taux_moyen, 1),
    }

    return render(request, 'dashboard/dashboard.html', context)