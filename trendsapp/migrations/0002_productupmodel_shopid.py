# Generated by Django 4.1.5 on 2023-03-31 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trendsapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productupmodel',
            name='shopid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
