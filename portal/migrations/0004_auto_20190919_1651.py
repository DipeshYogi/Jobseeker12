# Generated by Django 2.1 on 2019-09-19 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_auto_20190919_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='type',
            field=models.CharField(choices=[('Full time', 'Full time'), ('Part time', 'Part time'), ('Contract based', 'Contract based')], max_length=20, verbose_name='Job type'),
        ),
    ]
