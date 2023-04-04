# Generated by Django 4.1.5 on 2023-03-31 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trendsapp', '0003_cart_userid_wishlist_userid'),
    ]

    operations = [
        migrations.CreateModel(
            name='shopnotify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='usernotify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
