# Generated by Django 2.1.3 on 2019-01-26 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programari', '0007_detaliizi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programare',
            name='ora_programare',
            field=models.CharField(max_length=5, null=True),
        ),
    ]
