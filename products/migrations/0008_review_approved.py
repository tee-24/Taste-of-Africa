# Generated by Django 3.2.25 on 2024-12-17 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_contactmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
