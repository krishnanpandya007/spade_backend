# Generated by Django 3.2.9 on 2022-03-26 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverification',
            name='verification_code',
            field=models.CharField(default='jRkLP4t', max_length=7),
        ),
    ]