# Generated by Django 3.1.6 on 2021-04-08 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20210406_0524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='status',
            field=models.CharField(default='Pending', max_length=50),
        ),
    ]
