# Generated by Django 3.2.7 on 2021-09-06 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resist_temptation', '0003_temptation_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temptation',
            name='added_time',
            field=models.DateField(auto_now_add=True, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='temptation',
            unique_together=set(),
        ),
    ]
