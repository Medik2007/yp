# Generated by Django 5.0 on 2024-01-29 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_is_staff_alter_user_verification_sent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='img',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
    ]
