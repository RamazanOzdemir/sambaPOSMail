# Generated by Django 2.2.7 on 2019-11-21 13:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0013_auto_20191121_1612'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='outgoingemail',
            options={'ordering': ['date']},
        ),
        migrations.AlterField(
            model_name='person',
            name='uid',
            field=models.CharField(default=uuid.UUID('12c0a748-9b3b-48a5-9b88-2b00250df45e'), max_length=50),
        ),
    ]