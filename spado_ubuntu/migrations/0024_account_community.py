# Generated by Django 3.2.9 on 2022-03-05 03:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('spado_ubuntu', '0023_account_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='community',
            field=models.ManyToManyField(blank=True, related_name='community', to=settings.AUTH_USER_MODEL),
        ),
    ]