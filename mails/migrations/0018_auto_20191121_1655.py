# Generated by Django 2.2.7 on 2019-11-21 13:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0017_auto_20191121_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='uid',
            field=models.CharField(default=uuid.UUID('7cf4f1d2-0f8e-4e67-bc98-451677153c98'), max_length=50),
        ),
    ]
