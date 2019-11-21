# Generated by Django 2.2.7 on 2019-11-21 13:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0015_auto_20191121_1614'),
    ]

    operations = [
        migrations.CreateModel(
            name='LastMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(1989, 12, 31, 21, 0, tzinfo=utc))),
            ],
        ),
        migrations.AlterField(
            model_name='person',
            name='uid',
            field=models.CharField(default=uuid.UUID('4b26a706-0cc3-4dd2-a124-c76f50134666'), max_length=50),
        ),
    ]