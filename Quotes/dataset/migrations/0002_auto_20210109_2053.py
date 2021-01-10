# Generated by Django 3.1.3 on 2021-01-09 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('All', 'All')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('All', 'All')], max_length=10, null=True),
        ),
    ]
