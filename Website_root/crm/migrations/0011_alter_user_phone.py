# Generated by Django 5.0.1 on 2024-05-01 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0010_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Numer kontaktowy'),
        ),
    ]