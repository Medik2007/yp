# Generated by Django 5.0 on 2024-01-02 20:45

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chanels', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chanel',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
