# Generated by Django 2.1.3 on 2018-12-22 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribers',
            fields=[
                ('email_address', models.CharField(max_length=200, primary_key=True, serialize=False)),
            ],
        ),
    ]
