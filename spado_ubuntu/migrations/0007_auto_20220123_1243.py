# Generated by Django 3.2.9 on 2022-01-23 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spado_ubuntu', '0006_alter_account_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_pic',
            field=models.ImageField(default='default/default_2.jpg', upload_to='images/profile_pics/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image_1',
            field=models.FileField(blank=True, null=True, upload_to='images/posts/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image_2',
            field=models.FileField(blank=True, null=True, upload_to='images/posts/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image_3',
            field=models.FileField(blank=True, null=True, upload_to='images/posts/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image_4',
            field=models.FileField(blank=True, null=True, upload_to='images/posts/'),
        ),
    ]
