from django.shortcuts import render, redirect
from boanapp.pairs import assets


def visualize_data(request):
    context = {}
    context['pairs'] = assets
    context['hours'] = [hour for hour in range(24)]
    return render(request, 'index.html', context)


def get_data(request):
    return render(request, 'get-data.html')
