from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from boanapp.pairs import assets
from boanapp import labouchere, logic, pairs
import pandas as pd

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@cache_page(CACHE_TTL)
def visualize_data(request):
    context = {}
    hourly_profit = []
    hours = logic.get_moneies_list('AUDUSD', 2019, 7, 25)
    for hour in hours:
        profit = labouchere.ProphetC().get_profit(hours[hour])
        hourly_profit.append(profit)
    context['pairs'] = assets
    context['profits'] = hourly_profit
    context['hours'] = [hour for hour in range(24)]
    context['start_date'] = logic.get_start_date()
    context['end_date'] = logic.get_last_date()
    context['current_date'] = logic.get_start_date()
    return render(request, 'index.html', context)


@cache_page(CACHE_TTL)
def visulize_defined_data(request):
    context = {}
    hourly_profit = []
    date = request.POST.get('boan-date')
    split_date = date.split('/')
    hours = logic.get_moneies_list(request.POST.get(
        'asset'), split_date[2], split_date[0], split_date[1])
    for hour in hours:
        profit = labouchere.ProphetC().get_profit(hours[hour])
        hourly_profit.append(profit)
    context['pairs'] = assets
    context['profits'] = hourly_profit
    context['hours'] = [hour for hour in range(24)]
    context['start_date'] = logic.get_start_date()
    context['end_date'] = logic.get_last_date()
    context['current_date'] = request.POST.get('boan-date')
    context['current_asset'] = request.POST.get('asset')
    return render(request, 'index.html', context)


@cache_page(CACHE_TTL)
def tabular_data(request):
    context = {}
    # hourly_profit = []
    hourly_profit_dict = {}
    top_assets = pairs.assets[:10]
    all_dates = pd.date_range(start=logic.get_last_date(),
                              end=logic.get_start_date()).strftime("%m/%d/%Y").to_list()
    for date in all_dates:
        for asset in top_assets:
            hours = logic.get_moneies_list(
                asset, date.split('/')[2], date.split('/')[0], date.split('/')[1])
            for hour in hours:
                profit = labouchere.ProphetC().get_profit(hours[hour])
                hourly_profit_dict['date'] = [asset, profit]
    context['assets'] = top_assets
    context['hours'] = [hour for hour in range(24)]
    return render(request, 'tabular-data.html', context)
