from django.shortcuts import render, redirect
from boanapp.pairs import assets
from boanapp import labouchere, logic


def visualize_data(request):
    context = {}
    my_list = logic.get_moneies_list('EURUSD')

    context['pairs'] = assets
    context['hours'] = [hour for hour in range(24)]
    return render(request, 'index.html', context)


def get_data(request):
    return render(request, 'get-data.html')
