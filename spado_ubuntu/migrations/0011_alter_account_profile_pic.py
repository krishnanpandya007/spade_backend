# Generated by Django 3.2.9 on 2022-01-23 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spado_ubuntu', '0010_auto_20220123_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_pic',
            field=models.ImageField(default='default/default_2.jpg', upload_to='images/profile_pics/'),
        ),
    ]
