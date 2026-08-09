from django.shortcuts import render


def home_view(request):
    return render(request, "marketing_landing.html")
