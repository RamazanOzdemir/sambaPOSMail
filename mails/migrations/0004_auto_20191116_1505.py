# Generated by Django 2.2.7 on 2019-11-16 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0003_auto_20191116_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='personColor',
            field=models.CharField(choices=[('#e53935', 'Kırmızı'), ('#1976d2', 'Mavi'), ('#00796b', 'Yeşil'), ('#ffeb3b', 'Sarı'), ('#f4511e', 'Turuncu'), ('#546e7a', 'Gri'), ('#5e35b1', 'Mor')], default='#1976d2', max_length=15),
        ),
    ]
