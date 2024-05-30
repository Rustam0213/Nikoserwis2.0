from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth import get_user_model


class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Numer kontaktowy")
    email = models.EmailField(_("email address"), unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def get_user_applications(self):
        return Applications.objects.filter(from_who=self)

    class Meta:
        verbose_name = 'Użytkownika'
        verbose_name_plural = 'Użytkownicy'


class Applications(models.Model):
    completed = models.BooleanField(verbose_name="Wykonany" ,default=False)
    from_who = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Od kogo')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')
    desired_appointment_date = models.DateField(null=True, blank=True, verbose_name='Data spotkania')
    vin_code = models.CharField(max_length=17, verbose_name='VIN')
    reg_num = models.CharField(max_length=20, verbose_name='Numer rejestracyjny')
    mark = models.CharField(max_length=100, verbose_name='Marka')
    model = models.CharField(max_length=100, verbose_name='Model')
    year = models.CharField(max_length=100, verbose_name='Rok')
    displacement = models.CharField(max_length=100, verbose_name='Pojemność silnika')
    hp = models.CharField(max_length=100, verbose_name='KM')
    details = models.TextField(verbose_name='Szczegóły problemu')

    def __str__(self):
        return f"Wniosek od {self.from_who.username}"

    class Meta:
        verbose_name = 'Wniosek'
        verbose_name_plural = 'Wnioski'

