# Generated by Django 3.1.6 on 2021-03-16 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_match_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='is_feat',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tournament',
            name='sponsored_by',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
