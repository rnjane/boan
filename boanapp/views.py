import json
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
        if profit < 0:
            hourly_profit.append(0)
        else:
            hourly_profit.append(1)
    context['pairs'] = assets
    context['profits'] = hourly_profit
    context['hours'] = [hour for hour in range(24)]
    context['start_date'] = logic.get_start_date()
    context['end_date'] = logic.get_last_date()
    context['current_date'] = request.POST.get('boan-date')
    context['current_asset'] = request.POST.get('asset')
    return render(request, 'index.html', context)


# def choose_asset(request):
#     context = {}


# @cache_page(CACHE_TTL)
def tabular_data(request):
    context = {}
    top_assets = pairs.assets[:2]
    all_dates = pd.date_range(start=logic.get_last_date(),
                              end=logic.get_start_date()).strftime("%m/%d/%Y").to_list()

    total_profit_dict = {}
    for asset in top_assets:
        daily_profit_dict = {}
        # for date in all_dates:
        #     hours = logic.get_moneies_list(
        #         asset, date.split('/')[2], date.split('/')[0], date.split('/')[1])
        #     dips = 0
        #     for hour in hours:
        #         profit = labouchere.ProphetC().get_profit(hours[hour])
        #         if profit < 0:
        #             dips += 1
        #         daily_profit_dict[date] = dips

        total_profit_dict[asset] = daily_profit_dict
    x = {'AUDUSD': {'07/22/2019': 3, '07/23/2019': 8, '07/24/2019': 7, '07/25/2019': 7, '07/26/2019': 3},
         'AUDCAD': {'07/22/2019': 6, '07/23/2019': 8, '07/24/2019': 6, '07/25/2019': 7, '07/26/2019': 2}}
    context['data'] = x
    context['labels'] = json.dumps([i for i in x])
    context['vals'] = json.dumps(
        [{'AUDUSD': [3, 8, 7, 7, 3]}, {'AUDCAD': [6, 8, 6, 7, 2]}])
    context['dates2'] = json.dumps(["07/22/2019", "07/23/2019",
                                    "07/24/2019", "07/25/2019", "07/26/2019"])

    # context['datasets'] = r"[{
    #     label: '# of Votes',
    #     data: [12, 19, 3, 5, 2],
    #     backgroundColor: [
    #         'rgba(255, 99, 132, 0.2)',
    #         'rgba(54, 162, 235, 0.2)',
    #         'rgba(255, 206, 86, 0.2)',
    #         'rgba(75, 192, 192, 0.2)',
    #         'rgba(153, 102, 255, 0.2)',
    #         'rgba(255, 159, 64, 0.2)'
    #     ],
    #     borderColor: [
    #         'rgba(255, 99, 132, 1)',
    #         'rgba(54, 162, 235, 1)',
    #         'rgba(255, 206, 86, 1)',
    #         'rgba(75, 192, 192, 1)',
    #         'rgba(153, 102, 255, 1)',
    #         'rgba(255, 159, 64, 1)'
    #     ],
    #     borderWidth: 1
    # },
    #     {
    #     label: '# of Votes',
    #     data: [22, 29, 32, 25, 22],
    #     backgroundColor: [
    #         'rgba(255, 99, 132, 0.2)',
    #         'rgba(54, 162, 235, 0.2)',
    #         'rgba(255, 206, 86, 0.2)',
    #         'rgba(75, 192, 192, 0.2)',
    #         'rgba(153, 102, 255, 0.2)',
    #         'rgba(255, 159, 64, 0.2)'
    #     ],
    #     borderColor: [
    #         'rgba(255, 99, 132, 1)',
    #         'rgba(54, 162, 235, 1)',
    #         'rgba(255, 206, 86, 1)',
    #         'rgba(75, 192, 192, 1)',
    #         'rgba(153, 102, 255, 1)',
    #         'rgba(255, 159, 64, 1)'
    #     ],
    #     borderWidth: 1
    # }]"
    # context['dates'] = [list(i.keys())
    #                     for i in list(total_profit_dict.values())][0]
    # context['values'] = [i for i in hours_dict.values()]
    return render(request, 'tabular-data.html', context)
