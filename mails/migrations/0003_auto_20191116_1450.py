# Generated by Django 2.2.7 on 2019-11-16 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0002_auto_20191115_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incomingemail',
            name='date',
            field=models.DateTimeField(),
        ),
    ]