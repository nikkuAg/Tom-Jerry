# Generated by Django 3.2.8 on 2021-10-31 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_auto_20211031_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request_sent',
            name='status',
            field=models.CharField(default='empty', max_length=255, null=True),
        ),
    ]
