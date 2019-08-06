from django.shortcuts import render, redirect
from boanapp.pairs import assets
from boanapp import labouchere, logic


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


def get_data(request):
    return render(request, 'get-data.html')
