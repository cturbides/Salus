# Generated by Django 4.0.4 on 2022-04-16 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salusApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='person',
        ),
        migrations.AddField(
            model_name='patient',
            name='person',
            field=models.ManyToManyField(to='salusApp.person'),
        ),
    ]