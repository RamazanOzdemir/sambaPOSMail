# Generated by Django 2.2.7 on 2019-11-21 13:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0012_auto_20191119_1752'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='incomingemail',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='outgoingemail',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='person',
            name='uid',
            field=models.CharField(default=uuid.UUID('441c0fe6-46ea-4d5a-b554-70d2d76ee1fd'), max_length=50),
        ),
    ]
