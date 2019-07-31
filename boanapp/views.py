from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def visualize_data(request):
    return render(request, 'index.html')


def get_data(request):
    return render(request, 'get-data.html')
