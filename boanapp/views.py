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
    return render(request, 'index.html', context)


def get_data(request):
    return render(request, 'get-data.html')
