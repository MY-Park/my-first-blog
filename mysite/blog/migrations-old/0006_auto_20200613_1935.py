# Generated by Django 3.0.3 on 2020-06-13 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200613_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='interest',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
