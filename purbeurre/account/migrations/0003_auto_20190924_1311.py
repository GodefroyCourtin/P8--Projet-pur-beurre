# Generated by Django 2.2.5 on 2019-09-24 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20190924_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='postal_code',
            field=models.IntegerField(null=True),
        ),
    ]