# Generated by Django 2.1.3 on 2019-01-25 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Programare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=10)),
                ('nume', models.CharField(max_length=50)),
                ('max_programari', models.IntegerField(default=8)),
            ],
        ),
    ]
