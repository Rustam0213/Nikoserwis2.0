import random
import smtplib
from email.mime.text import MIMEText

from axes.decorators import axes_dispatch
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.cache import cache
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from django.views import View
from django.urls import reverse

from .forms import ApplicationForm, UserCreationForm, UserProfileForm, VerificationCodeForm
from .models import Applications, User


@login_required
def user_profile(request):
    user = request.user

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('user_profile')
    else:
        profile_form = UserProfileForm(instance=user)

    return render(request, 'user_profile.html', {'profile_form': profile_form})

@login_required
def application_details(request, application_id):
    application = get_object_or_404(Applications, pk=application_id)
    if application.from_who != request.user:
        raise Http404("Error")

    return render(request, 'application_details.html', {'application': application})


@login_required
def profile(request):
    user = request.user
    user_applications = user.get_user_applications().order_by('-date_created')

    return render(request, 'profile.html', {'user_applications': user_applications})


@login_required
def wiadomosc(request):
    user = request.user

    has_uncompleted_applications = Applications.objects.filter(from_who=user, completed=False).exists()

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.from_who = user
            application.save()

            # URL админ панели
            admin_url = request.build_absolute_uri(reverse('admin:index'))

            # Загрузка и рендеринг шаблона
            html_content = render_to_string('email_template.html', {'user': user, "application":application, 'admin_url': admin_url})
            text_content = strip_tags(html_content) 

            # Создание и отправка email
            email = EmailMultiAlternatives(
                subject=f'Nowy wniosek od {user.first_name} {user.last_name}',
                body=text_content,
                from_email='nikoserwisbot@gmail.com',
                to=['rdvelihanov1245@gmail.com'],
            )
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False)

            return redirect('profile')
    else:
        form = ApplicationForm()

    return render(request, 'wiadomosc.html', {'user': user, 'form': form, 'has_uncompleted_applications': has_uncompleted_applications})

class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {'form': UserCreationForm()}
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            
            last_sent_time = cache.get(email + '_last_sent_time')
            if last_sent_time is None or (timezone.now() - last_sent_time).seconds >= 120:
                rand = random.randint(1000, 9999)
                request.session['verification_code'] = rand
                request.session['email'] = email
                request.session['password'] = form.cleaned_data['password1']
                request.session['first_name'] = form.cleaned_data['first_name']
                request.session['last_name'] = form.cleaned_data['last_name']
                request.session['phone'] = form.cleaned_data['phone']

                html_content = render_to_string('kod_email.html', {"rand": rand})
                text_content = strip_tags(html_content)

                email_message = EmailMessage(
                    "Twój kod weryfikacyjny",
                    html_content,
                    'nikoserwisbot@gmail.com',
                    [email],
                )
                email_message.content_subtype = "html"  # Устанавливаем тип контента как HTML
                email_message.send()

                cache.set(email + '_last_sent_time', timezone.now(), 120)  # 120 секунд = 2 минуты

                return redirect('kod')
            else:
                messages.error(request, 'Kod już był wysłany. Spróbuj ponownie za 2 minuty.')

        context = {'form': form}
        return render(request, self.template_name, context)


def kod(request):
    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            get_code = form.cleaned_data.get('verification_code')
            random_code = request.session.get('verification_code')
            email = request.session.get('email')
            password = request.session.get('password')
            first_name = request.session.get('first_name')
            last_name = request.session.get('last_name')
            phone = request.session.get('phone')

            if get_code == random_code:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone
                )

                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)

                    del request.session['verification_code']
                    del request.session['email']
                    del request.session['password']
                    del request.session['first_name']
                    del request.session['last_name']
                    del request.session['phone']

                    return redirect('profile')
                else:
                    messages.error(request, 'Stworzenie użytkownika nie udało się')
            else:
                messages.error(request, 'Wpisałeś niepoprawny kod')
        else:
            messages.error(request, 'Błąd formularzu')
    else:
        form = VerificationCodeForm()

    return render(request, 'registration/kod.html', {'form': form})


class CustomLoginView(View):
    template_name = 'registration/login.html'

    @axes_dispatch
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {'form': AuthenticationForm()}
        return render(request, self.template_name, context)

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
        context = {'form': form}
        return render(request, self.template_name, context)