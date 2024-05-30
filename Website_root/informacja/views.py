from django.shortcuts import render, redirect
from django.urls import reverse
from crm.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import News, Promotion, Humor
from django.http import HttpResponse
import smtplib
from email.mime.text import MIMEText
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from crm.models import Applications
from django.core.serializers import serialize
from django.http import JsonResponse

@staff_member_required
def calendar(request):
    applications = Applications.objects.all()
    events = []
    for application in applications:
        admin_url = reverse('admin:crm_applications_change', args=(application.id,))
        events.append({
            'title': f'Wniosek od: {application.from_who.username}',
            'start': application.desired_appointment_date.strftime('%Y-%m-%d'),
            'admin_url': admin_url
        })
    return render(request, 'calendar.html', {'events': events})


def main_page(request):
    return render(request, 'index.html')

def nowosci(request):
    news = News.objects.all().order_by('-date')
    return render(request, 'wiadomosci.html', {'news': news})

def promocje(request):
    promotion = Promotion.objects.all().order_by('-date')
    return render(request, 'promocje.html', {'promotion':promotion})

def humor(request):
    humor = Humor.objects.all().order_by('-date')
    return render(request, 'humor.html', {'humor':humor})

def rejestracja(request):
    return render(request, 'rejestracja.html')

def log_in(request):
    return render(request, 'login.html')

def polityka(request):
    return render(request, 'polityka-prywatnosci.html')

def error(request):
    return render(request, "error.html")